import os

import pytest
from chalice import Chalice

os.environ['ARCUS_API_KEY'] = 'test'
os.environ['ARCUS_SECRET_KEY'] = 'test'
os.environ['TOPUP_API_KEY'] = 'test'
os.environ['TOPUP_SECRET_KEY'] = 'test'

from app import app as chalice_app  # isort:skip # NOQA


@pytest.fixture
def app() -> Chalice:
    return chalice_app
