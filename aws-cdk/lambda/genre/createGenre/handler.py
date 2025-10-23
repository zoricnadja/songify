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
    #         'headers': CORS_HEADERS,
    #         'body': json.dumps({'message': 'Access Denied'})
    #     }
    try:
        body = json.loads(event.get('body', '{}'))
        genre = body.get('genre')
        
        if not genre:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Missing genre'}), 'headers': CORS_HEADERS}
        
        if table.get_item(Key={'genre': genre}).get('Item'):
            return {'statusCode': 409, 'body': json.dumps({'message': 'Genre already exists'}), 'headers': CORS_HEADERS}
        
        table.put_item(Item={'genre': genre})
        return {'statusCode': 201, 'body': json.dumps({'message': 'Genre created'}), 'headers': CORS_HEADERS}
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}

