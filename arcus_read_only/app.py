import json
import os

from arcus.client import Client

arcus_api_key = os.environ['ARCUS_API_KEY']
arcus_secret_key = os.environ['ARCUS_SECRET_KEY']


def make_response(status_code: int, body: dict) -> dict:
    return {'statusCode': status_code, 'body': json.dumps(body)}


def lambda_handler(event, context):
    try:
        sandbox = event['headers']['X-ARCUS-SANDBOX'] == 'true'
        client = Client(arcus_api_key, arcus_secret_key, sandbox=sandbox)
        path = event['path']
        if (
            event['queryStringParameters']
            and 'page' in event['queryStringParameters']
        ):
            path += f'?page={event["queryStringParameters"]["page"]}'
        response = client.get(path)
        return make_response(200, response)
    except Exception as ex:
        return make_response(400, dict(message='Bad Request'))
