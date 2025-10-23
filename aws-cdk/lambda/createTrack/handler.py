import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

tracks_table_name = os.environ['TRACKS_TABLE']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

tracks_table = dynamodb.Table(tracks_table_name)

def lambda_handler(event, context):
    try: 
        body = json.loads(event.get('body', '{}'))
        track_id = str(uuid.uuid4())
        item = {
            "track_id": track_id,
            "artists": body["artists"],
            "artist": body["artists"][0],
            "genres": body["genres"],
            "track_name": body["trackName"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "album_id": body.get('album', 'Unknown'),
        }

        tracks_table.put_item(Item=item)

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps(item),
            MessageAttributes={
                "contentType": {
                    "DataType": "String",
                    "Value": "track"
                }
            },
            Subject="New track published"
        )

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Track created successfully", "item": item})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }
