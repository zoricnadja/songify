import json
import os

import boto3
from boto3.dynamodb.conditions import Key

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ARTISTS_TABLE_NAME'])

ARTIST_ID_INDEX = 'ArtistIDIndex'

def handler(event, context):
    artist_id = event.get('pathParameters', {}).get('id')
    if not artist_id:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing Artist ID'}), 'headers': CORS_HEADERS}
    try:
        response = table.query(
            IndexName=ARTIST_ID_INDEX,
            KeyConditionExpression=Key('artist_id').eq(artist_id)
        )
        items = response.get('Items', [])
        if not items:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Artist not found'}), 'headers': CORS_HEADERS}
        artist = {
            'id': artist_id,
            'name': items[0].get('name'),
            'biography': items[0].get('biography'),
            'genres': items[0].get('genres', [])
        }
        return {'statusCode': 200, 'body': json.dumps(artist), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}
