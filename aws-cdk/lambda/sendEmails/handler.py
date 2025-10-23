import json
import boto3
import os
from boto3.dynamodb.conditions import Key
import logging

# Kreiranje loggera
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) 
dynamodb = boto3.resource('dynamodb')
subscriptions_table = dynamodb.Table(os.environ['SUBSCRIPTIONS_TABLE'])
SES_SOURCE_EMAIL = os.environ["SES_SOURCE_EMAIL"]
region = os.environ.get("SES_REGION", os.environ.get("AWS_REGION", "eu-central-1"))
ses = boto3.client("ses", region_name=region)
sent_emails = []

def send_email(recipient, subject, body):
    try:
        response = ses.send_email(
            Source=SES_SOURCE_EMAIL,
            Destination={"ToAddresses": [recipient]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}},
            }
        )
        sent_emails.append(recipient)
        logger.debug(f"Email sent to {recipient}, MessageId: {response['MessageId']}")
    except Exception as e:
        logger.debug(f"Failed to send email to {recipient}: {e}")

def lambda_handler(event, context):
    for record in event["Records"]:
        message = json.loads(record["Sns"]["Message"])
        attributes = record["Sns"].get("MessageAttributes", {})

        content_type = attributes.get("contentType", {}).get("StringValue", "track")
        genres = message.get("genres", [])
        artists = message.get("artists", [])
        track_name = message.get('track_name', 'Untitled')
        created_at = message.get('created_at', 'N/A')
        all_genre_subs = []
        for genre in genres:
            all_genre_subs += subscriptions_table.query(
                KeyConditionExpression=Key("target").eq(f"genre#{genre}")
            ).get("Items", [])

        all_artist_subs = []
        for artist in artists:    
            all_artist_subs += subscriptions_table.query(
                KeyConditionExpression=Key("target").eq(f"artist#{artist}")
            ).get("Items", [])
        users = all_artist_subs + all_genre_subs
        logger.debug(f"useri : {users}")
        if not users:
            logger.debug("No subscribers found.")
            continue
        for user in users:
            email = user.get("user_email")
            if email and not email in sent_emails:
                send_email(
                    email,
                    f"New {content_type} from {artist}",
                    f"A new {content_type} '{track_name}' was published on {created_at} by {artist} in genre {genre}!"
                )

    headers = {"Access-Control-Allow-Origin": "*"}
    return {"statusCode": 200, "headers": headers, "body": "Emails sent"}
