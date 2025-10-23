from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
import os
import json

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3', region_name=os.environ['REGION'], endpoint_url=os.environ['S3_ENDPOINT_URL'])

track_table = dynamodb.Table(os.environ['TRACKS_TABLE_NAME'])
artist_table = dynamodb.Table(os.environ['ARTISTS_TABLE_NAME'])
album_table = dynamodb.Table(os.environ['ALBUMS_TABLE_NAME'])

ARTIST_ID_INDEX = 'ArtistIDIndex'
ALBUM_ID_INDEX = 'AlbumIDIndex'

TRACK_ALBUM_INDEX = 'AlbumIndex'

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}
TRACK_ID_INDEX = 'TrackIDIndex'
BUCKET_NAME = os.environ['TRACKS_BUCKET_NAME']

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def handler(event, context):
    artist_id = (event.get('queryStringParameters', {}) or {}).get('artist_id')
    album_id = (event.get('queryStringParameters', {}) or {}).get('album_id')

    try:
        if artist_id:
            response = track_table.query(
                KeyConditionExpression=Key('artist_id').eq(artist_id)
            )
            items = response.get('Items', [])
            return {'statusCode': 200, 'body': json.dumps(get_tracks(items), default=decimal_default), 'headers': CORS_HEADERS}
        elif album_id:
            response = track_table.query(
                IndexName=TRACK_ALBUM_INDEX,
                KeyConditionExpression=Key('album_id').eq(album_id)
            )
            items = response.get('Items', [])
            return {'statusCode': 200, 'body': json.dumps(get_tracks(items), default=decimal_default), 'headers': CORS_HEADERS}
        else:
            response = track_table.scan()
            items = response.get('Items', [])
            tracks = get_tracks(items)
            return {'statusCode': 200, 'body': json.dumps(tracks, default=decimal_default), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}


def get_tracks(items):
    tracks = {}
    for item in items:
        track_id = item['track_id']
        if track_id not in tracks:
            image_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': BUCKET_NAME, 'Key': item.get('image_key')},
                ExpiresIn=3600
            )

            track_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': BUCKET_NAME, 'Key': item.get('track_key')},
                ExpiresIn=3600
            )

            tracks[track_id] = {
                'id': track_id,
                'title': item.get('title'),
                'genres': item.get('genres', []),
                'imageUrl': image_url,
                'artists': get_artists([item.get('artist_id')]),
                'album': get_album(item.get('album_id')) if item.get('album_id') else None,
                'trackUrl': track_url,
                'file': item.get('file_info')
            }
        else:
            tracks[track_id]['artists'].extend(get_artists([item.get('artist_id')]))
    return list(tracks.values())


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

def get_album(album_id):
    response = album_table.query(
        IndexName=ALBUM_ID_INDEX,
        KeyConditionExpression=Key('album_id').eq(album_id)
    )

    items = response.get('Items', [])

    if not items:
        return None

    return {
        'id': album_id,
        'title': items[0].get('title'),
        'artists': get_artists(items[0].get('artist_ids', [])),
        'genres': list({item['genre'] for item in items})
    }
