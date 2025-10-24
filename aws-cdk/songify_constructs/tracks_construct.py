from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sns as sns
from constructs import Construct
from utils.create_lambda import create_lambda_function

class TracksConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        api: apigateway.RestApi,
        authorizer,
        score_table: dynamodb.Table,
        tracks_table: dynamodb.Table,
        artists_table: dynamodb.Table,
        albums_table: dynamodb.Table,
        tracks_bucket: s3.Bucket,
        content_created_topic: sns.Topic,
        region='eu-central-1',
    ):
        super().__init__(scope, id)

        presign_upload_lambda = create_lambda_function(
            self,
            "PresignUploadLambda",
            handler="handler.handler",
            include_dir="lambda/s3_presign_upload",
            layers=[],
            environment={
                "TRACKS_BUCKET_NAME": tracks_bucket.bucket_name,
                "REGION": region,
                "S3_ENDPOINT_URL": f"https://s3.{region}.amazonaws.com"
            }
        )
        tracks_bucket.grant_write(presign_upload_lambda)

        # Rate Track Lambda (POST /tracks/{trackId}/score)
        rate_track_lambda = create_lambda_function(
            self,
            "RateTrackLambda",
            "handler.lambda_handler",
            "lambda/score/rateTrack",
            [],
            {
                "SCORE_TABLE": score_table.table_name,
                "TRACK_TABLE": tracks_table.table_name,
            }
        )
        score_table.grant_read_write_data(rate_track_lambda)
        tracks_table.grant_read_data(rate_track_lambda)

        # Get Track Score Lambda (GET /tracks/{trackId}/score)
        get_track_score_lambda = create_lambda_function(
            self,
            "GetTrackScoreLambda",
            "handler.lambda_handler",
            "lambda/score/getTrackScore",
            [],
            {
                "SCORE_TABLE": score_table.table_name,
            }
        )
        score_table.grant_read_data(get_track_score_lambda)

        create_track_lambda = create_lambda_function(
            self,
            "CreateTrackLambda",
            handler="handler.handler",
            include_dir="lambda/track/create_track",
            layers=[],
            environment={"TRACKS_TABLE_NAME": tracks_table.table_name,
                         "CONTENT_CREATED_TOPIC_ARN": content_created_topic.topic_arn,}
        )
        tracks_table.grant_read_write_data(create_track_lambda)
        tracks_bucket.grant_read_write(create_track_lambda)

        create_track_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "sns:CreateTopic",
                    "sns:Subscribe",
                    "sns:ListTopics",
                    "sns:Publish",
                    "sns:GetTopicAttributes",
                ],
                resources=["*"],
            )
        )
        content_created_topic.grant_publish(create_track_lambda)

        get_tracks_lambda = create_lambda_function(
            self,
            "GetTracksLambda",
            handler="handler.handler",
            include_dir="lambda/track/get_tracks",
            layers=[],
            environment={
                "TRACKS_TABLE_NAME": tracks_table.table_name,
                "ARTISTS_TABLE_NAME": artists_table.table_name,
                "ALBUMS_TABLE_NAME": albums_table.table_name,
                "TRACKS_BUCKET_NAME": tracks_bucket.bucket_name,
                "REGION": region,
                "S3_ENDPOINT_URL": f"https://s3.{region}.amazonaws.com"
            }
        )
        tracks_table.grant_read_data(get_tracks_lambda)
        artists_table.grant_read_data(get_tracks_lambda)
        albums_table.grant_read_data(get_tracks_lambda)
        tracks_bucket.grant_read_write(get_tracks_lambda)

        get_track_lambda = create_lambda_function(
            self,
            "GetTrackLambda",
            handler="handler.handler",
            include_dir="lambda/track/get_track",
            layers=[],
            environment={"TRACKS_TABLE_NAME": tracks_table.table_name}
        )
        tracks_table.grant_read_data(get_track_lambda)

        update_track_lambda = create_lambda_function(
            self,
            "UpdateTrackLambda",
            handler="handler.handler",
            include_dir="lambda/track/update_track",
            layers=[],
            environment={"TRACKS_TABLE_NAME": tracks_table.table_name}
        )
        tracks_table.grant_read_write_data(update_track_lambda)
        tracks_bucket.grant_read_write(update_track_lambda)

        delete_track_lambda = create_lambda_function(
            self,
            "DeleteTrackLambda",
            handler="handler.handler",
            include_dir="lambda/track/delete_track",
            layers=[],
            environment={
                "TRACKS_TABLE_NAME": tracks_table.table_name,
                "TRACKS_BUCKET_NAME": tracks_bucket.bucket_name,
                "REGION": region,
                "S3_ENDPOINT_URL": f"https://s3.{region}.amazonaws.com"
            }
        )
        tracks_table.grant_read_write_data(delete_track_lambda)
        tracks_bucket.grant_read_write(delete_track_lambda)

        s3_resource = api.root.add_resource("s3")
        presign_resource = s3_resource.add_resource("presign-upload")

        presign_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(presign_upload_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        tracks_resource = api.root.add_resource("tracks")

        tracks_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(
                get_tracks_lambda,
                proxy=True,
                request_parameters={
                    "integration.request.querystring.artist_id": "method.request.querystring.artist_id",
                    "integration.request.querystring.album_id": "method.request.querystring.album_id",
                }
            ),
            request_parameters={
                "method.request.querystring.artist_id": False,
                "method.request.querystring.album_id": False,
            },
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        tracks_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(create_track_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        track_item_resource = tracks_resource.add_resource("{id}")

        track_item_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(get_track_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        track_item_resource.add_method(
            "PUT",
            apigateway.LambdaIntegration(update_track_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        track_item_resource.add_method(
            "DELETE",
            apigateway.LambdaIntegration(delete_track_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        score_resource = track_item_resource.add_resource("score")

        score_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(rate_track_lambda, proxy=True),
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO
        )

        score_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(get_track_score_lambda, proxy=True),
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO
        )