import json
import os
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from datetime import datetime

track_table_name = os.environ["TRACK_TABLE"]
score_table_name = os.environ["SCORE_TABLE"]

dynamodb = boto3.resource("dynamodb")
track_table = dynamodb.Table(track_table_name)
score_table = dynamodb.Table(score_table_name)

def lambda_handler(event, context):
    headers = {"Access-Control-Allow-Origin": "*"}

    claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
    role = claims.get("custom:role")
    user_id = claims.get('sub')
    if role != "user":
        return {
            "statusCode": 403,
            "headers": headers,
            "body": json.dumps({"message":"Forbidden: Insufficient permissions"})
        }

    try:
        body = json.loads(event.get('body', '{}'))
        track_id = event['pathParameters']['id']
        score = body.get('score')
        if not track_id:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Track id is required"})
            }
        
        response = track_table.query(
            IndexName='TrackIDIndex',
            KeyConditionExpression=Key('track_id').eq(track_id)
        )
        items = response.get("Items")
        if not items:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Track is not found"})
            }
        track = items[0]
        
        if score is None:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Score is required"})
            }

        score_table.put_item(
            Item={
                "user_id": user_id,
                "track_id": track_id,
                "genre": track['genre'],
                "score": Decimal(str(score)),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "Score saved successfully"})
        }

    except Exception as e:
        print("Error saving score:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }