import pytest
from main_run import create_app
from flask import Flask


@pytest.fixture
def client() -> Flask:
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    test_app = create_app(with_secutiry=False)
    test_app.testing = True
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    tester = test_app.test_client()

    yield tester
