import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ALBUMS_TABLE_NAME'])

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}
ALBUM_ID_INDEX = 'AlbumIDIndex'

def handler(event, context):
    # claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    # role = claims.get('custom:role')
    # if role != 'admin':
    #     return {'statusCode': 403, 'body': json.dumps({'message': 'Access Denied'}), 'headers': CORS_HEADERS}

    album_id = event.get('pathParameters', {}).get('id')
    if not album_id:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing Album ID'}), 'headers': CORS_HEADERS}

    try:
        response = table.query(
            IndexName=ALBUM_ID_INDEX,
            KeyConditionExpression=Key('album_id').eq(album_id)
        )

        items = response.get('Items', [])
        if not items:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Album not found'}), 'headers': CORS_HEADERS}

        for item in items:
            table.delete_item(Key={'genre': item['genre'], 'album_id': album_id})

        return {'statusCode': 200, 'body': json.dumps({'message': 'Album deleted'}), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}

