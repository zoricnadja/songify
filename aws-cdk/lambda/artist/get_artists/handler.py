import json
import os

import boto3
from boto3.dynamodb.conditions import Key

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ARTISTS_TABLE_NAME'])

def handler(event, context):
    genre = (event.get('queryStringParameters') or {}).get('genre')
    try:
        if genre:
            response = table.query(
                KeyConditionExpression=Key('genre').eq(genre)
            )
            artists = []
            for item in response.get('Items', []):
                artists.append({
                    'id': item['artist_id'],
                    'name': item.get('name'),
                    'biography': item.get('biography'),
                    'genres': item.get('genres')
                })
            return {'statusCode': 200, 'body': json.dumps(artists), 'headers': CORS_HEADERS}
        else:
            response = table.scan()
            items = response.get('Items', [])
            artists = {}
            for item in items:
                artist_id = item['artist_id']
                if artist_id not in artists:
                    artists[artist_id] = {
                        'id': artist_id,
                        'name': item.get('name'),
                        'biography': item.get('biography'),
                        'genres': item.get('genres')
                    }
            return {'statusCode': 200, 'body': json.dumps(list(artists.values())), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}
