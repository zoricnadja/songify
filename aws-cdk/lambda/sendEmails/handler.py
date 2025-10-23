import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
subscriptions_table = dynamodb.Table(os.environ['SUBSCRIPTIONS_TABLE'])
SES_SOURCE_EMAIL = os.environ["SES_SOURCE_EMAIL"]
region = os.environ.get("SES_REGION", os.environ.get("AWS_REGION", "eu-central-1"))
ses = boto3.client("ses", region_name=region)

def send_email(recipient, subject, body):
    ses.send_email(
        Source=SES_SOURCE_EMAIL,
        Destination={"ToAddresses": [recipient]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}},
        }
    )

def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["Sns"]["Message"])
        attributes = record["Sns"].get("MessageAttributes", {})

        content_type = attributes.get("contentType", {}).get("Value", "song")
        genres = message.get("genres", [])
        artists = message.get("artists", [])
        track_name = message.get('track_name', 'Untitled')
        created_at = message.get('created_at', 'N/A')

        for genre in genres:
            genre_subs = subscriptions_table.query(
                KeyConditionExpression=Key("target").eq(f"genre#{genre}")
            ).get("Items", [])
            
        for artist in artists:    
            artist_subs = subscriptions_table.query(
                KeyConditionExpression=Key("target").eq(f"artist#{genre}")
            ).get("Items", [])

        users = artist_subs + genre_subs
        if not users:
            print("No subscribers found.")
            continue

        for user in users:
            email = user.get("email")
            if email:
                send_email(
                    email,
                    f"New {content_type} from {artist}",
                    f"A new {content_type} '{track_name}' was published on {created_at} by {artist} in genre {genre}!"
                )

    return {"statusCode": 200, "body": "Emails sent"}
