import json
import os
import uuid

import boto3

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ARTISTS_TABLE_NAME'])

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
        name = body.get('name')
        biography = body.get('biography')
        genres = body.get('genres', [])
        if not name or not biography or not genres:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Missing required fields'}), 'headers': CORS_HEADERS}
        artist_id = str(uuid.uuid4())
        for genre in genres:
            table.put_item(Item={
                'genre': genre,
                'artist_id': artist_id,
                'name': name,
                'biography': biography,
                'genres': genres
            })
        return {'statusCode': 201, 'body': json.dumps({'artist_id': artist_id}), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}

