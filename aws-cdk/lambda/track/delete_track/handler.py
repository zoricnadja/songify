import boto3
import os
import json
from boto3.dynamodb.conditions import Key

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TRACKS_TABLE_NAME'])
s3 = boto3.client('s3', region_name=os.environ.get('REGION'), endpoint_url=os.environ.get('S3_ENDPOINT_URL'))

BUCKET_NAME = os.environ.get('TRACKS_BUCKET_NAME')
TRACK_ID_INDEX = 'TrackIDIndex'

def handler(event, context):
    # claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    # role = claims.get('custom:role')
    # if role != 'admin':
    #     return {'statusCode': 403, 'body': json.dumps({'message': 'Access Denied'}), 'headers': CORS_HEADERS}

    track_id = event.get('pathParameters', {}).get('id')
    if not track_id:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing artist_id or track_id'}), 'headers': CORS_HEADERS}
    try:
        response = table.query(
            IndexName=TRACK_ID_INDEX,
            KeyConditionExpression=Key('track_id').eq(track_id)
        )
        items = response.get('Items', [])
        if not items:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Track not found'}), 'headers': CORS_HEADERS}

        for item in items:
            table.delete_item(Key={'artist_id': item['artist_id'], 'track_id': item['track_id']})

            if item.get('image_key'):
                s3.delete_object(Bucket=BUCKET_NAME, Key=item['image_key'])
            if item.get('track_key'):
                s3.delete_object(Bucket=BUCKET_NAME, Key=item['track_key'])

        return {'statusCode': 200, 'body': json.dumps({'message': 'Track deleted'}), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}

