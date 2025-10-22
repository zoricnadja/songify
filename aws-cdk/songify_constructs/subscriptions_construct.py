from constructs import Construct
from aws_cdk import aws_apigateway as apigateway,aws_iam as iam, aws_lambda as _lambda, aws_dynamodb as dynamodb
from utils.create_lambda import create_lambda_function

class SubscriptionsConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        api: apigateway.RestApi,
        authorizer,
        subscriptions_table: dynamodb.Table,
        genres_table: dynamodb.Table,
        artists_table: dynamodb.Table
    ):
        super().__init__(scope, id)

        subscriptions_api_resource = api.root.add_resource("subscriptions")

        # Create Subscription
        create_subscription_lambda = create_lambda_function(
            self,
            "CreateSubscriptionLambda",
            "handler.lambda_handler",
            "lambda/createSubscription",
            [],
            {"SUBSCRIPTIONS_TABLE": subscriptions_table.table_name,
            "GENRES_TABLE": genres_table.table_name,
            "ARTISTS_TABLE": artists_table.table_name,}
        )
        subscriptions_table.grant_read_write_data(create_subscription_lambda)
        genres_table.grant_read_write_data(create_subscription_lambda)
        artists_table.grant_read_write_data(create_subscription_lambda)

        subscriptions_api_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(create_subscription_lambda, proxy=True),
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO
        )

        # Get Subscriptions
        get_subscriptions_lambda = create_lambda_function(
            self,
            "GetSubscriptionsLambda",
            "handler.lambda_handler",
            "lambda/getSubscriptionsByUser",
            [],
            {"SUBSCRIPTIONS_TABLE": subscriptions_table.table_name}
        )
        subscriptions_table.grant_read_write_data(get_subscriptions_lambda)

        subscriptions_api_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(get_subscriptions_lambda, proxy=True),
            authorizer=authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO
        )

        # # Delete artist
        # delete_subscription_lambda = create_lambda_function(
        #     self,
        #     "DeleteSubscriptionLambda",
        #     "handler.lambda_handler",
        #     "lambda/deleteSubscription",
        #     [],
        #     {
        #      "SUBSCRIPTIONS_TABLE": subscriptions_table.table_name,
        #     }
        # )
        # subscriptions_table.grant_read_write_data(delete_subscription_lambda)

        # subscriptions_id_resource = subscriptions_api_resource.add_resource("{id}")
        # subscriptions_id_resource.add_method(
        #     "DELETE",
        #     apigateway.LambdaIntegration(delete_subscription_lambda, proxy=True),
        #     authorizer=authorizer,
        #     authorization_type=apigateway.AuthorizationType.COGNITO
        # )