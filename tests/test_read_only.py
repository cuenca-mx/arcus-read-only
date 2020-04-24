import json
from unittest import mock

import pytest
from pytest_chalice.handlers import RequestHandler


class Account:
    def __init__(self):
        self.name: str = "Cuenca"
        self.balance: float = 3232.32
        self.minimum_balance: float = 0.0
        self.currency: str = "MXN"


def test_healthcheck(client: RequestHandler) -> None:
    response = client.get('/')

    assert response.status_code == 200
    assert response.json == dict(greeting="I'm healthy")


def test_read_only_accounts(client: RequestHandler) -> None:
    with mock.patch(
        'chalicelib.resources.arcus_read_only.Client'
    ) as ClientTesting:
        ClientTesting.return_value.accounts = dict(
            primary=Account(), topup=Account(),
        )

        headers: dict = {'X-ARCUS-SANDBOX': 'true'}
        response = client.get('/account', headers=headers)

        assert response.status_code == 200
        assert response.json["statusCode"] == 200
        assert "body" in response.json
        accounts_response: dict = json.loads(response.json["body"])
        assert accounts_response["primary"] is not None
        assert accounts_response["topup"] is not None


def test_with_parameters(client: RequestHandler) -> None:
    with mock.patch(
        'chalicelib.resources.arcus_read_only.Client'
    ) as ClientTesting:
        ClientTesting.return_value.get.return_value = dict(resp="Success!!!")

        headers: dict = {'X-ARCUS-SANDBOX': 'true'}
        response = client.get('/test?page=1', headers=headers)

        assert response.status_code == 200
        assert response.json["statusCode"] == 200
        assert "body" in response.json
        success_resp: dict = json.loads(response.json["body"])
        assert success_resp["resp"] == "Success!!!"


def test_catch_exception(client: RequestHandler) -> None:
    with mock.patch(
        'chalicelib.resources.arcus_read_only.Client'
    ) as ClientTesting:
        ClientTesting.return_value.get.return_value.raiseError.side_effect = (
            Exception()
        )

        headers: dict = {'X-ARCUS-SANDBOX': 'true'}
        response = client.get('/test?page=1', headers=headers)

        assert response.status_code == 200
        assert response.json["statusCode"] == 400
        assert "body" in response.json
        resp: dict = json.loads(response.json["body"])
        assert resp["message"] == "Bad Request"
