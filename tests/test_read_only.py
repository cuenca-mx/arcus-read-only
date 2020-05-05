import json
from unittest import mock

import pytest
from arcus.exc import InvalidAuth
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
        assert response.json["primary"] is not None
        assert response.json["topup"] is not None


def test_with_parameters(client: RequestHandler) -> None:
    with mock.patch(
        'chalicelib.resources.arcus_read_only.Client'
    ) as ClientTesting:
        ClientTesting.return_value.get.return_value = dict(resp="Success!!!")

        headers: dict = {'X-ARCUS-SANDBOX': 'true'}
        response = client.get('/test?page=1', headers=headers)

        assert response.status_code == 200
        assert response.json["resp"] == "Success!!!"


def test_catch_exception(client: RequestHandler) -> None:
    with mock.patch(
        'chalicelib.resources.arcus_read_only.Client'
    ) as ClientTesting:
        ClientTesting.return_value.get.side_effect = Exception()

        headers: dict = {'X-ARCUS-SANDBOX': 'true'}
        response = client.get('/test?page=1', headers=headers)

        assert response.status_code == 400
        assert response.json["message"] == "Bad Request"


def test_catch_exception_auth(client: RequestHandler) -> None:
    with mock.patch(
        'chalicelib.resources.arcus_read_only.Client'
    ) as ClientTesting:
        ClientTesting.return_value.get.side_effect = InvalidAuth()

        headers: dict = {'X-ARCUS-SANDBOX': 'true'}
        response = client.get('/test?page=1', headers=headers)

        assert response.status_code == 401
        assert response.json["message"] == "Invalid Authentication Token"
