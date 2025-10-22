import json
import os
import uuid
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from datetime import datetime

subscriptions_table_name = os.environ["SUBSCRIPTIONS_TABLE"]
artists_table_name = os.environ["ARTISTS_TABLE"]
genres_table_name = os.environ["GENRES_TABLE"]
dynamodb = boto3.resource("dynamodb")
subscriptions_table = dynamodb.Table(subscriptions_table_name)
genres_table = dynamodb.Table(genres_table_name)
artists_table = dynamodb.Table(artists_table_name)

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
        target_type = body.get('targetType')
        target_id = body.get('targetId')
        target_name = body.get('targetName')
        if not target_id or not target_type:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Target is required"})
            }
        if target_type == 'artist':
            response = artists_table.query(
                IndexName='ArtistIDIndex',
                KeyConditionExpression=Key('artist_id').eq(target_id)
            )
        elif target_type == 'genre':
            response = genres_table.query(
                KeyConditionExpression=Key("genre").eq(target_id)
            )
        else: 
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Target type must be genre or artist"})
            }
        
        items = response.get("Items")
        if not items:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"message": "Target is not found"})
            }
        target = items[0]

        subscriptions_table.put_item(
            Item={
                "subscription_id": str(uuid.uuid4()),
                "target": f"{target_type}#{target_id}",
                "user_id": user_id,
                "subscription_type": target_type,
                "target_name": target['artist_name'] if target_type == 'artist' else target['genre'],
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

        return {
            "statusCode": 201,
            "headers": headers,
            "body": json.dumps({"message": "Subscription created successfully"})
        }

    except Exception as e:
        print("Error saving score:", str(e))
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }