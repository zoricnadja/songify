from aws_cdk import CfnOutput, Duration, RemovalPolicy, Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subs
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as _lambda
from constructs import Construct

from songify_constructs.tracks_construct import TracksConstruct
from songify_constructs.subscriptions_construct import SubscriptionsConstruct
from songify_constructs.emails_construct import EmailsConstruct

class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, project_name: str = "songify",
                 read_capacity: int = 1, write_capacity: int = 1, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ----------------------------
        # DynamoDB tables
        # ----------------------------
        # Genres
        genres_table = dynamodb.Table(
            self, "GenresTable",
            table_name=f"{project_name}-genres",
            partition_key=dynamodb.Attribute(name="genre", type=dynamodb.AttributeType.STRING),
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Artists
        artists_table = dynamodb.Table(
            self, "ArtistsTable",
            table_name=f"{project_name}-artists",
            partition_key=dynamodb.Attribute(name="genre", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="artist_id", type=dynamodb.AttributeType.STRING),
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            removal_policy=RemovalPolicy.DESTROY
        )

        artists_table.add_global_secondary_index(
            index_name="ArtistIDIndex",
            partition_key=dynamodb.Attribute(name="artist_id", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL,
            read_capacity=read_capacity,
            write_capacity=write_capacity
        )

        # Albums
        albums_table = dynamodb.Table(
            self, "AlbumsTable",
            table_name=f"{project_name}-albums",
            partition_key=dynamodb.Attribute(name="genre", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="album_id", type=dynamodb.AttributeType.STRING),
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            removal_policy=RemovalPolicy.DESTROY,
        )

        albums_table.add_global_secondary_index(
            index_name="AlbumIDIndex",
            partition_key=dynamodb.Attribute(name="album_id", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL,
            read_capacity=read_capacity,
            write_capacity=write_capacity
        )

        # Tracks
        tracks_table = dynamodb.Table(
            self, "TracksTable",
            table_name=f"{project_name}-tracks",
            partition_key=dynamodb.Attribute(name="artist_id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="track_id", type=dynamodb.AttributeType.STRING),
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            removal_policy=RemovalPolicy.DESTROY,
        )

        tracks_table.add_global_secondary_index(
            index_name="AlbumIndex",
            partition_key=dynamodb.Attribute(name="album_id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="track_id", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL,
            read_capacity=read_capacity,
            write_capacity=write_capacity
        )

        tracks_table.add_global_secondary_index(
            index_name="TrackIDIndex",
            partition_key=dynamodb.Attribute(name="track_id", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL,
            read_capacity=read_capacity,
            write_capacity=write_capacity
        )

        # Scores
        scores_table = dynamodb.Table(
            self, "ScoresTable",
            table_name=f"{project_name}-scores",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="track_id", type=dynamodb.AttributeType.STRING),
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            removal_policy=RemovalPolicy.DESTROY,
        )

        scores_table.add_global_secondary_index(
            index_name="ScoreGenreIndex",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="genre", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL,
            read_capacity=read_capacity,
            write_capacity=write_capacity
        )

        # Subscriptions
        subscriptions_table = dynamodb.Table(
            self, "SubscriptionsTable",
            table_name=f"{project_name}-subscriptions",
            partition_key=dynamodb.Attribute(name="target", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
            read_capacity=read_capacity,
            write_capacity=write_capacity,
            removal_policy=RemovalPolicy.DESTROY,
        )

        subscriptions_table.add_global_secondary_index(
            index_name="SubUserIdIndex",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL,
            read_capacity=read_capacity,
            write_capacity=write_capacity
        )
        
        subscriptions_table.add_global_secondary_index(
            index_name="SubIdIndex",
            partition_key=dynamodb.Attribute(name="subscription_id", type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL,
            read_capacity=read_capacity,
            write_capacity=write_capacity
        )

        #Topics 
        # topics_table = dynamodb.Table(
        #     self, "TopicsTable",
        #     partition_key=dynamodb.Attribute(name="target", type=dynamodb.AttributeType.STRING),
        #     table_name="TopicsTable",
        #     removal_policy=RemovalPolicy.DESTROY
        # )

        # ----------------------------
        # Cognito User Pool
        # ----------------------------
        user_pool = cognito.UserPool(
            self, "UserPool",
            user_pool_name=f"{project_name}-user-pool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(username=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=False),
                given_name=cognito.StandardAttribute(required=True, mutable=True),
                family_name=cognito.StandardAttribute(required=True, mutable=True),
                birthdate=cognito.StandardAttribute(required=False, mutable=True),
            ),
            custom_attributes={
                "role": cognito.StringAttribute(mutable=True)
            },
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False
            ),
                account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            mfa=cognito.Mfa.OFF,
            removal_policy=RemovalPolicy.DESTROY,
        )

        user_pool_client = user_pool.add_client(
            "UserPoolClient",
            user_pool_client_name=f"{project_name}-app-client",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
            ),
            access_token_validity=Duration.hours(1),
            id_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(5),
            prevent_user_existence_errors=True,
            enable_token_revocation=True
        )

        # Lambda for auto-confirm and auto-verify email
        pre_sign_up_lambda = _lambda.Function(
            self,
            "PreSignUpLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.main",
            code=_lambda.Code.from_inline(
                """def main(event, context):
                    event['response']['autoConfirmUser'] = True
                    event['response']['autoVerifyEmail'] = True
                    return event
                """
            )
        )

        user_pool.add_trigger(cognito.UserPoolOperation.PRE_SIGN_UP, pre_sign_up_lambda)

        # Outputs
        CfnOutput(self, "UserPoolId", value=user_pool.user_pool_id, description="User Pool ID")
        CfnOutput(self, "UserPoolClientId", value=user_pool_client.user_pool_client_id,
                  description="User Pool Client ID")
        
        # ----------------------------
        # REST API
        # ----------------------------
        api = apigateway.RestApi(
            self, "songifyApi",
            rest_api_name="songifyApi",
            deploy_options=apigateway.StageOptions(stage_name="dev", throttling_rate_limit=100, throttling_burst_limit=200),
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
            ),
            endpoint_configuration=apigateway.EndpointConfiguration(
                types=[apigateway.EndpointType.REGIONAL] 
            )
        )

        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self, "CognitoAuthorizer",
            cognito_user_pools=[user_pool],
        )

        TracksConstruct(self, "TracksConstruct", api, authorizer, scores_table, tracks_table)
        SubscriptionsConstruct(self, "SubscriptionsConstruct", api, authorizer, subscriptions_table, genres_table, artists_table)
        # EmailsConstruct(self, "EmailsConstruct", subscriptions_table, topic)
