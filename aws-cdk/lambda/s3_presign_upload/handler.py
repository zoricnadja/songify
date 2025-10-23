import boto3
import os
import json
import uuid

s3 = boto3.client('s3', region_name=os.environ['REGION'], endpoint_url=os.environ['S3_ENDPOINT_URL'])

BUCKET_NAME = os.environ['TRACKS_BUCKET_NAME']
CORS_HEADERS = {'Access-Control-Allow-Origin': '*'}
FILE_PREFIX = 'tracks'

def handler(event, context):
    # claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', {})
    # if not claims.get('sub'):
    #     return {'statusCode': 403, 'body': json.dumps({'message': 'Access Denied'}), 'headers': CORS_HEADERS}
    try:
        body = json.loads(event.get('body', '{}'))
        file_name = body.get('fileName')
        file_type = body.get('fileType')
        if not file_name or not file_type:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Missing file name or type'}), 'headers': CORS_HEADERS}

        key = f"{FILE_PREFIX}/{uuid.uuid4()}_{file_name}"
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': key,
                'ContentType': file_type
            },
            ExpiresIn=600
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'url': presigned_url, 'key': key}),
            'headers': CORS_HEADERS
        }
    except Exception as e:
        return {'statusCode': 500, 'body': str(e), 'headers': CORS_HEADERS}

