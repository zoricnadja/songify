from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key
import os
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TRACKS_TABLE_NAME'])
CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

TRACK_ID_INDEX = 'TrackIDIndex'

def handler(event, context):
    track_id = event.get('pathParameters', {}).get('id')
    if not track_id:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing track ID'}), 'headers': CORS_HEADERS}

    try:
        response = table.query(
            IndexName=TRACK_ID_INDEX,
            KeyConditionExpression=Key('track_id').eq(track_id)
        )
        items = response.get('Items', [])
        if not items:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Track not found'}), 'headers': CORS_HEADERS}

        return {'statusCode': 200, 'body': json.dumps([items[0]][0], default=decimal_default), 'headers': CORS_HEADERS}
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

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError
