import json
import os

from arcus.client import Client

arcus_api_key = os.environ['ARCUS_API_KEY']
arcus_secret_key = os.environ['ARCUS_SECRET_KEY']


def make_response(status_code: int, body: dict) -> dict:
    return {'statusCode': status_code, 'body': json.dumps(body)}


def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        try:
            print(arcus_api_key)
            print(arcus_secret_key)
            sandbox = event['headers']['X-Arcus-Sandbox'] == 'true'
            client = Client(arcus_api_key, arcus_secret_key, sandbox=sandbox)
            response = client.get(event['path'])
            return make_response(200, response)
        except Exception as ex:
            print(f'Error: {ex}')
            return make_response(400, dict(message='Bad Request'))
    else:
        return make_response(405, dict(message='Method Not Allowed'))
