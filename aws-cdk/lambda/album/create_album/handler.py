import json
import os
import uuid

import boto3

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ALBUMS_TABLE_NAME'])

def handler(event, context):
    # claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    # role = claims.get('custom:role')
    # if role != 'admin':
    #     return {
    #         'statusCode': 403,
    #         'body': json.dumps({'message': 'Access Denied'}),
    #         'headers': CORS_HEADERS
    #     }
    try:
        body = json.loads(event.get('body', '{}'))

        title = body.get('title')
        artist_ids = body.get('artistIds')

        genres = body.get('genres', [])
        if not title or not artist_ids or not genres:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Missing required fields'}), 'headers': CORS_HEADERS}

        album_id = str(uuid.uuid4())
        for genre in genres:
            table.put_item(Item={
                'genre': genre,
                'album_id': album_id,
                'title': title,
                'artist_ids': artist_ids,
                'genres': genres
            })
        return {'statusCode': 201, 'body': json.dumps({'album_id': album_id}), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}

