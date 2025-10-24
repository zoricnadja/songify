import boto3
import os
import json
import uuid

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TRACKS_TABLE_NAME'])
sns = boto3.client('sns')
content_created_topic_arn = os.environ["CONTENT_CREATED_TOPIC_ARN"]

def handler(event, context):
    claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    role = claims.get('custom:role')
    if role != 'admin':
        return {
            'statusCode': 403,
            'body': json.dumps({'message': 'Forbidden: Admins only'}),
            'headers': CORS_HEADERS
        }

    try:
        body = json.loads(event.get('body', '{}'))
        title = body.get('title')
        genres = body.get('genres', [])
        image_key = body.get('imageKey')
        track_key = body.get('trackKey')
        artist_ids = body.get('artistIds', [])
        album_id = body.get('albumId')
        file_info = body.get('file')
        if not title or not genres or not image_key or not artist_ids or not track_key: # or not file_name or not file_type or not file_size:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Missing required fields'}), 'headers': CORS_HEADERS}

        track_id = str(uuid.uuid4())

        for artist_id in artist_ids:
            item = {
                'artist_id': artist_id,
                'track_id': track_id,
                'title': title,
                'genres': genres,
                'image_key': image_key,
                'track_key': track_key,
                'file_info': file_info,
            }

            if album_id:
                item['album_id'] = album_id

            table.put_item(Item=item)
            
        sns.publish(
            TopicArn=content_created_topic_arn,
            Message=json.dumps(item),
            Subject=f"New track created: {item['track_name']}"
        )
        return {'statusCode': 201, 'body': json.dumps({'track_id': track_id}), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}
