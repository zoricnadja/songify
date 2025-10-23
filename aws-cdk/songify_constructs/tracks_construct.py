from constructs import Construct
from aws_cdk import (
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    # aws_sns as sns,
    aws_iam as iam
)
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
    ):
        super().__init__(scope, id)

        tracks_api_resource = api.root.add_resource("tracks")

        # Create Track Lambda (POST /tracks)
        create_track_lambda = create_lambda_function(
            self,
            "CreateTrackLambda",
            "handler.lambda_handler",
            "lambda/createTrack",
            [],
            {
                "TRACKS_TABLE": tracks_table.table_name,
            }
        )
        tracks_table.grant_write_data(create_track_lambda)
        # SNS permission, runtime-created topic ARNs 
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

        tracks_api_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(create_track_lambda, proxy=True),
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO
        )

        track_id_resource = tracks_api_resource.add_resource("{id}")

        score_resource = track_id_resource.add_resource("score")

        # Rate Track Lambda (POST /tracks/{trackId}/score)
        rate_track_lambda = create_lambda_function(
            self,
            "RateTrackLambda",
            "handler.lambda_handler",
            "lambda/rateTrack",
            [],
            {
                "SCORE_TABLE": score_table.table_name,
                "TRACK_TABLE": tracks_table.table_name,
            }
        )
        score_table.grant_read_write_data(rate_track_lambda)
        tracks_table.grant_read_data(rate_track_lambda)

        score_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(rate_track_lambda, proxy=True),
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO
        )

        # Get Track Score Lambda (GET /tracks/{trackId}/score)
        get_track_score_lambda = create_lambda_function(
            self,
            "GetTrackScoreLambda",
            "handler.lambda_handler",
            "lambda/getTrackScore",
            [],
            {
                "SCORE_TABLE": score_table.table_name,
            }
        )
        score_table.grant_read_data(get_track_score_lambda)

        score_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(get_track_score_lambda, proxy=True),
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO
        )