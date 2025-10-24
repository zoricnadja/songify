import json
import os
import uuid
import boto3
from datetime import datetime

subscriptions_table_name = os.environ["SUBSCRIPTIONS_TABLE"]
dynamodb = boto3.resource("dynamodb")
subscriptions_table = dynamodb.Table(subscriptions_table_name)
sns = boto3.client('sns')

def get_or_create_topic(topic_name):
    return sns.create_topic(Name=topic_name)['TopicArn']

def lambda_handler(event, context):
    headers = {"Access-Control-Allow-Origin": "*"}

    claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
    role = claims.get("custom:role")
    user_id = claims.get('sub')
    user_email = claims.get('email')
    if role != "user":
        return {
            "statusCode": 403,
            "headers": headers,
            "body": json.dumps({"message":"Forbidden: Insufficient permissions"})
        }

    try:
        body = json.loads(event.get('body', '{}'))
        target_type = body.get('targetType')
        target_id = body.get('targetId')
        target_name = body.get('targetName')
        if not target_id or not target_type:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Target is required"})
            }
        target_key = f"{target_type}_{target_id}"
        topic_arn = get_or_create_topic(target_key)

        subscription_response = sns.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint=user_email, ReturnSubscriptionArn=True)

        subscription_arn = subscription_response.get("SubscriptionArn", "PendingConfirmation")

        subscriptions_table.put_item(
            Item={
                "subscription_id": str(uuid.uuid4()),
                "target": target_key,
                "user_id": user_id,
                "user_email": user_email,
                "subscription_type": target_type,
                "target_name":target_name,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "subscription_arn": subscription_arn
            }
        )

        message = "Subscription created successfully."
        if subscription_arn == "PendingConfirmation":
            message += " Please check your email to confirm the subscription."

        return {
            "statusCode": 201,
            "headers": headers,
            "body": json.dumps({
                "message": "Subscribed",
                "target": target_key,
                "topicArn": topic_arn,
                "subscription_arn": subscription_arn
            })
        }

    except Exception as e:
        print("Error saving score:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }