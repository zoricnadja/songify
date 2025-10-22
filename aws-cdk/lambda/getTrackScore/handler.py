import json
import os

import boto3
from datetime import datetime
from decimal import Decimal

table_name = os.environ["SCORE_TABLE"]
dynamodb = boto3.resource("dynamodb")
score_table = dynamodb.Table(table_name)

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
        track_id = event.get("pathParameters", {}).get("id")

        if not track_id:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Track id is required"})
            }

        response = score_table.get_item(
            Key={
                "user_id": user_id,
                "track_id": track_id
            }
        )

        item = response.get("Item")

        if not item:
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "user_id": user_id,
                    "track_id": track_id,
                    "score": 0,
                    "timestamp": datetime.min
                }, default=decimal_default)
            }

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(item, default=decimal_default)
        }

    except Exception as e:
        print("Error loading score:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)}, default=decimal_default)
        }