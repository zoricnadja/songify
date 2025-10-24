from aws_cdk import (
    aws_sns as sns,
    aws_iam as iam,
    aws_sns_subscriptions as subs,
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
            "lambda/subscription/notifySubscribers",
            [],
            {},
        )
        
        notify_lambda.add_to_role_policy(
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
        content_created_topic.add_subscription(subs.LambdaSubscription(notify_lambda))
