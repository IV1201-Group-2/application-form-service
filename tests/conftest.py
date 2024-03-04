import os

import pytest
from testcontainers.postgres import PostgresContainer  # type: ignore

from app.app import create_app, database


@pytest.fixture(scope='session')
def postgres():
    with PostgresContainer('postgres:latest') as postgres:
        yield postgres


@pytest.fixture(scope='function')
def app_with_client(postgres):
    os.environ['DATABASE_URL'] = postgres.get_connection_url()
    flask_app = create_app()
    flask_app.config.update({
        'TESTING': True,
        'JWT_SECRET_KEY': 'your-test-secret-key',
    })

    with flask_app.app_context():
        database.create_all()
        database.session.commit()

    with flask_app.test_client() as testing_client:
        yield flask_app, testing_client

    with flask_app.app_context():
        database.session.remove()
        database.drop_all()
