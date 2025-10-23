import json
import os

import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from decimal import Decimal

table_name = os.environ["SUBSCRIPTIONS_TABLE"]
dynamodb = boto3.resource("dynamodb")
subscriptions_table = dynamodb.Table(table_name)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

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
    try:
        response = subscriptions_table.query(
            IndexName='SubUserIdIndex',
                KeyConditionExpression=Key('user_id').eq(user_id)
        )

        items = response.get("Items")
        subscriptions = []
        for item in items:
            subscription = {
                'id': item['subscription_id'],
                'targetType': item['subscription_type'],
                'targetName': item['target_name'],
                'createdAt': item['created_at'],
            }
            subscriptions.append(subscription)
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(subscriptions)
        }

    except Exception as e:
        print("Error loading score:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)}, default=decimal_default)
        }