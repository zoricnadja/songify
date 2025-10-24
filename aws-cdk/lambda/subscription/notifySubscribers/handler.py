import json
import boto3

sns = boto3.client("sns")
CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

def get_or_create_topic(topic_name):
    response = sns.create_topic(Name=topic_name)
    return response["TopicArn"]


def lambda_handler(event, context):
    for record in event["Records"]:
        sns_message = record["Sns"]["Message"]
        subject = record["Sns"].get("Subject", "New content available")

        try:
            item = json.loads(sns_message)
        except json.JSONDecodeError:
            print("Could not parse SNS message, skipping.")
            continue

        for genre in item.get("genres", []):
            topic_arn = get_or_create_topic(f"genre_{genre}")
            sns.publish(
                TopicArn=topic_arn,
                Message=sns_message,
                Subject=subject,
            )

        for artist in item.get("artists", []):
            topic_arn = get_or_create_topic(f"artist_{artist}")
            sns.publish(
                TopicArn=topic_arn,
                Message=sns_message,
                Subject=subject,
            )

    return {"statusCode": 200, "headers": CORS_HEADERS, "body": json.dumps({"message": "Notifications sent."})}
