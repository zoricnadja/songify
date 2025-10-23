import boto3
import os
import json
from datetime import datetime, UTC
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TRACKS_TABLE_NAME'])
CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}
TRACK_ID_INDEX = 'TrackIDIndex'

def handler(event, context):
    claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    role = claims.get('custom:role')
    if role != 'admin':
        return {'statusCode': 403, 'body': json.dumps({'message': 'Forbidden: Admins only'}), 'headers': CORS_HEADERS}
    artist_id = event.get('pathParameters', {}).get('artist_id')
    track_id = event.get('pathParameters', {}).get('track_id')
    if not artist_id or not track_id:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing artist_id or track_id'}), 'headers': CORS_HEADERS}
    try:
        body = json.loads(event.get('body', '{}'))
        title = body.get('title')
        genres = body.get('genres', [])
        image_url = body.get('image_url')
        artists = body.get('artists', [])
        album_id = body.get('album_id')
        track_file_url = body.get('track_file_url')
        file_name = body.get('file_name')
        file_type = body.get('file_type')
        file_size = body.get('file_size')
        now = datetime.now(UTC).isoformat()
        # Get all records for track_id
        response = table.query(
            IndexName=TRACK_ID_INDEX,
            KeyConditionExpression=Key('track_id').eq(track_id)
        )
        items = response.get('Items', [])
        if not items:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Track not found'}), 'headers': CORS_HEADERS}
        # Update all records for this track_id
        for item in items:
            pk = item['artist_id']
            sk = item['track_id']
            table.update_item(
                Key={'artist_id': pk, 'track_id': sk},
                UpdateExpression="SET title=:t, genres=:g, image_url=:i, artists=:a, album_id=:al, track_file_url=:tf, file_name=:fn, file_type=:ft, file_size=:fs, updated_at=:u",
                ExpressionAttributeValues={
                    ':t': title if title else item.get('title'),
                    ':g': genres if genres else item.get('genres'),
                    ':i': image_url if image_url else item.get('image_url'),
                    ':a': artists if artists else item.get('artists'),
                    ':al': album_id if album_id else item.get('album_id'),
                    ':tf': track_file_url if track_file_url else item.get('track_file_url'),
                    ':fn': file_name if file_name else item.get('file_name'),
                    ':ft': file_type if file_type else item.get('file_type'),
                    ':fs': file_size if file_size else item.get('file_size'),
                    ':u': now
                }
            )
        return {'statusCode': 200, 'body': json.dumps({'message': 'Track updated'}), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}
