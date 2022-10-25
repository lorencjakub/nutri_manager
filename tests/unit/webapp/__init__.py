import pytest
from main_run import create_app
from flask import Flask


@pytest.fixture
def client() -> Flask:
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    test_app = create_app()
    test_app.testing = True
    tester = test_app.test_client()

    yield tester
