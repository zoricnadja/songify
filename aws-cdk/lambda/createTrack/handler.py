import json
import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

tracks_table_name = os.environ['TRACKS_TABLE']

tracks_table = dynamodb.Table(tracks_table_name)

def get_or_create_topic(topic_name):
    topic_arn = sns.create_topic(Name=topic_name)['TopicArn']
    return topic_arn

def lambda_handler(event, context):
    headers = {"Access-Control-Allow-Origin": "*"}
    try: 
        body = json.loads(event.get('body', '{}'))
        track_id = str(uuid.uuid4())
        item = {
            "track_id": track_id,
            "artists": body["artists"],
            "artist_id": body["artist_id"],
            "genres": body["genres"],
            "track_name": body["trackName"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "album_id": body.get('album', 'Unknown'),
        }

        tracks_table.put_item(Item=item)

        for genre in body["genres"]:
            topic_arn = get_or_create_topic(f"genre_{genre}")
            sns.publish(
                TopicArn=topic_arn,
                Message=json.dumps(item),
                Subject=f"New track in {genre}"
            )

        for artist in body["artists"]:
            topic_arn = get_or_create_topic(f"artist_{artist}")
            sns.publish(
                TopicArn=topic_arn,
                Message=json.dumps(item),
                Subject=f"New track from {artist}"
            )

        return {
            "statusCode": 201,
            "headers": headers,
            "body": json.dumps({"message": "Track created successfully", "item": item})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
