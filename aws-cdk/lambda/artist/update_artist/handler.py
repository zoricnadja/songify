import json
import os

import boto3
from boto3.dynamodb.conditions import Key

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ARTISTS_TABLE_NAME'])

artist_id_index = 'ArtistIDIndex'

def handler(event, context):
    # claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    # role = claims.get('custom:role')
    # if role != 'admin':
    #     return {
    #         'statusCode': 403,
    #         'body': json.dumps({'message': 'Access Denied'}),
    #         'headers': CORS_HEADERS
    #     }
    artist_id = event.get('pathParameters', {}).get('id')
    if not artist_id:
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing Artist ID'}), 'headers': CORS_HEADERS}
    try:
        body = json.loads(event.get('body', '{}'))
        name = body.get('name')
        biography = body.get('biography')
        genres = body.get('genres', [])
        if not name or not biography or not genres:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Missing required fields'}), 'headers': CORS_HEADERS}

        response = table.query(
            IndexName=artist_id_index,
            KeyConditionExpression=Key('artist_id').eq(artist_id)
        )
        artists = response.get('Items', [])
        if not artists:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Artist not found'}), 'headers': CORS_HEADERS}

        for genre in genres:
            if genre not in artists[0]['genres']:
                table.put_item(Item={
                    'genre': genre,
                    'artist_id': artist_id,
                    'name': name,
                    'biography': biography,
                    'genres': genres
                })

        for artist in artists:
            if artist['genre'] not in genres:
                table.delete_item(Key={'genre': artist['genre'], 'artist_id': artist_id})
            else:
                table.update_item(
                    Key={'genre': artist['genre'], 'artist_id': artist_id},
                    UpdateExpression="SET #n = :name, biography = :biography, genres = :genres",
                    ExpressionAttributeNames={
                        '#n': 'name'
                    },
                    ExpressionAttributeValues={
                        ':name': name,
                        ':biography': biography,
                        ':genres': genres
                    }
                )
        return {'statusCode': 200, 'body': json.dumps({'message': 'Artist updated'}), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}

