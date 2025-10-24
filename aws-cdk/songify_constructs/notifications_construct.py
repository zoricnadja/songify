from aws_cdk import (
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_iam as iam,
)
from constructs import Construct
from utils.create_lambda import create_lambda_function


class NotificationsConstruct(Construct):

    def __init__(self, scope: Construct, id: str, tracks_table, subscriptions_table, content_created_topic: sns.Topic):
        super().__init__(scope, id)

        notify_lambda = create_lambda_function(
            self,
            "NotifySubscribersLambda",
            "handler.lambda_handler",
            "lambda/notifySubscribers",
            [],
            {
                "SUBSCRIPTIONS_TABLE": subscriptions_table.table_name,
                "SES_REGION": "eu-central-1",
                "SES_SOURCE_EMAIL": "zoricnadja03@gmail.com",
            },
        )

        subscriptions_table.grant_read_data(notify_lambda)

        notify_lambda.add_to_role_policy(
            iam.PolicyStatement(actions=["ses:SendEmail", "ses:SendRawEmail"], resources=["*"])
        )

        content_created_topic.add_subscription(subs.LambdaSubscription(notify_lambda))
