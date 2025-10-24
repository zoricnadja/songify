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
    genre = (event.get('queryStringParameters') or {}).get('genre')
    try:
        if genre:
            response = album_table.query(
                KeyConditionExpression=Key('genre').eq(genre)
            )
            items = response.get('Items', [])
            return {'statusCode': 200, 'body': json.dumps(get_albums(items)), 'headers': CORS_HEADERS}
        else:
            response = album_table.scan()
            items = response.get('Items', [])
            return {'statusCode': 200, 'body': json.dumps(get_albums(items)), 'headers': CORS_HEADERS}
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

def get_albums(items):
    albums = {}
    for item in items:
        album_id = item['album_id']
        if album_id not in albums:
            albums[album_id] = {
                'id': album_id,
                'title': item.get('title'),
                'artists': get_artists(item.get('artist_ids', [])),
                'genres': item.get('genres')
            }
    return list(albums.values())