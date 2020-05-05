import json
import os

from arcus.client import Client
from arcus.exc import InvalidAuth
from chalice import Response

from .base import app

arcus_api_key: str = os.environ['ARCUS_API_KEY']
arcus_secret_key: str = os.environ['ARCUS_SECRET_KEY']
topup_api_key: str = os.environ['TOPUP_API_KEY']
topup_secret_key: str = os.environ['TOPUP_SECRET_KEY']


@app.route('/{event}', methods=['GET'])
def lambda_handler(event: str) -> dict:
    request = app.current_request

    try:
        sandbox: bool = request.headers['X-ARCUS-SANDBOX'] == 'true'
        client: Client = Client(
            arcus_api_key,
            arcus_secret_key,
            topup_api_key,
            topup_secret_key,
            sandbox=sandbox,
        )
        path: str = event
        if request.query_params and 'page' in request.query_params:
            path += f'?page={request.query_params["page"]}'
        if path == 'account':
            response: dict = client.accounts
            response['primary'] = vars(response['primary'])
            response['topup'] = vars(response['topup'])
        else:
            response = client.get(f'/{path}')
        return Response(body=response, status_code=200,)
    except InvalidAuth:
        return Response(
            body=dict(message='Invalid Authentication Token'), status_code=401,
        )
    except Exception as ex:
        return Response(
            body=dict(message='Bad Request', exception=str(ex)),
            status_code=400,
        )
