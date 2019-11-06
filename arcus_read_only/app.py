import json
import os

import sentry_sdk
from sentry_sdk import capture_exception
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

from arcus.client import Client

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    integrations=[AwsLambdaIntegration()]
)

arcus_api_key = os.environ['ARCUS_API_KEY']
arcus_secret_key = os.environ['ARCUS_SECRET_KEY']
topup_api_key = os.environ['TOPUP_API_KEY']
topup_secret_key = os.environ['TOPUP_SECRET_KEY']


def make_response(status_code: int, body: dict) -> dict:
    return {'statusCode': status_code, 'body': json.dumps(body)}


def lambda_handler(event, context):
    try:
        sandbox = event['headers']['X-ARCUS-SANDBOX'] == 'true'
        client = Client(
            arcus_api_key,
            arcus_secret_key,
            topup_api_key,
            topup_secret_key,
            sandbox=sandbox
        )
        path = event['path']
        if (
            event['queryStringParameters']
            and 'page' in event['queryStringParameters']
        ):
            path += f'?page={event["queryStringParameters"]["page"]}'
        if path == '/account':
            response = client.accounts
        else:
            response = client.get(path)
        return make_response(200, response)
    except Exception as ex:
        capture_exception(ex)
        return make_response(400, dict(message='Bad Request'))
