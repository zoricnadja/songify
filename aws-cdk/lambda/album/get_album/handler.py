import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
album_table = dynamodb.Table(os.environ['ALBUMS_TABLE_NAME'])
artist_table = dynamodb.Table(os.environ['ARTISTS_TABLE_NAME'])

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

ALBUM_ID_INDEX = 'AlbumIDIndex'
ARTIST_ID_INDEX = 'ArtistIDIndex'

def handler(event, context):
    album_id = event.get('pathParameters', {}).get('id')
    if not album_id:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing Album ID'}), 'headers': CORS_HEADERS}
    try:
        response = album_table.query(
            IndexName=ALBUM_ID_INDEX,
            KeyConditionExpression=Key('album_id').eq(album_id)
        )

        items = response.get('Items', [])
        if not items:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Album not found'}), 'headers': CORS_HEADERS}

        album = {
            'id': album_id,
            'title': items[0].get('title'),
            'artists': get_artists(items[0].get('artist_ids', [])),
            'genres': list({item['genre'] for item in items})
        }
        return {'statusCode': 200, 'body': json.dumps(album), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}

def get_artists(artist_ids):
    artists = []
    for artist_id in artist_ids:
        response = artist_table.query(
            IndexName=ARTIST_ID_INDEX,
            KeyConditionExpression=Key('artist_id').eq(artist_id)
        )
        items = response.get('Items', [])
        if items:
            artist = items[0]
            artists.append({
                'id': artist_id,
                'name': artist.get('name'),
                'biography': artist.get('biography'),
                'genres': artist.get('genres', [])
            })
    return artists
