import json
import os

import boto3

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['GENRES_TABLE_NAME'])

def handler(event, context):
    # claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    # role = claims.get('custom:role')
    # if role != 'admin':
    #     return {
    #         'statusCode': 403,
    #         'body': json.dumps({'message': 'Forbidden: Admins only'}),
    #         'headers': CORS_HEADERS
    #     }
    try:
        genre = event.get('pathParameters', {}).get('genre')
        body = json.loads(event.get('body', '{}'))
        new_genre = body.get('genre')
        if not genre or not new_genre:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Bad Request'}), 'headers': CORS_HEADERS}
        table.delete_item(Key={'genre': genre})
        table.put_item(Item={'genre': new_genre})
        return {'statusCode': 200, 'body': json.dumps({'message': 'Genre updated'}), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e)}

