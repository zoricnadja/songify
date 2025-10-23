from constructs import Construct
from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_iam as iam, 
    aws_dynamodb as dynamodb,
    aws_ses as ses
)
from utils.create_lambda import create_lambda_function

class EmailsConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        subscriptions_table: dynamodb.Table,
        topic: sns.Topic,
    ):
        super().__init__(scope, id)

        ses.EmailIdentity(
            self,
            "MyEmailIdentity",
            identity=ses.Identity.email("zoricnadja03@gmail.com")
        )
        # Send Email Lambda
        send_emails_lambda = create_lambda_function(
            self,
            "SendEmails",
            "handler.lambda_handler",
            "lambda/sendEmails",
            [],
            {
                "SUBSCRIPTIONS_TABLE": subscriptions_table.table_name,
                "SES_REGION": "eu-central-1",
                "SES_SOURCE_EMAIL": "zoricnadja03@gmail.com"
            }
        )
        subscriptions_table.grant_read_data(send_emails_lambda)

        send_emails_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]
            )
        )

        topic.add_subscription(subs.LambdaSubscription(send_emails_lambda))