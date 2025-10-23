import json
import os

import boto3

CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('GENRES_TABLE_NAME')
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        response = table.scan()
        genres = [{'name': genre['genre']} for genre in response.get('Items', [])]
        return {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps(genres)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(e),
            'headers': CORS_HEADERS
        }

