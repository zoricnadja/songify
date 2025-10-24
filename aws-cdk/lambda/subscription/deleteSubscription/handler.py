import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

subscriptions_table_name = os.environ["SUBSCRIPTIONS_TABLE"]
dynamodb = boto3.resource("dynamodb")
sns = boto3.client('sns')
subscriptions_table = dynamodb.Table(subscriptions_table_name)

def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
    }

    claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
    user_id = claims.get('sub')
    if not user_id:
        return {
            "statusCode": 403,
            "headers": headers,
            "body": json.dumps({"message":"Forbidden: Insufficient permissions"})
        }
    
    subscription_id = event.get("pathParameters", {}).get("id")
    if not subscription_id:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"message": "Missing subscription id in path"})
        }
    
    try:
        response = subscriptions_table.query(
            IndexName="SubIdIndex",
            KeyConditionExpression=Key("subscription_id").eq(subscription_id),
        )
        items = response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "headers": headers,
                "body": json.dumps({"message": "Subscription not found"})
            }

        subscription = items[0]
        subscription_arn = subscription.get("subscription_arn")
        if subscription_arn and subscription_arn != "PendingConfirmation":
            try:
                sns.unsubscribe(SubscriptionArn=subscription_arn)
                print(f"Unsubscribed SNS ARN: {subscription_arn}")
            except Exception as sns_error:
                print(f"Error unsubscribing SNS: {sns_error}")
        subscriptions_table.delete_item(
            Key={
                "target": subscription["target"],
                "user_id": subscription["user_id"]
            }
        )

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": f"Subscription {subscription_id} deleted successfully"})
        }

    except Exception as e:
        print("DynamoDB error:", e)
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": "Internal server error"})
        }