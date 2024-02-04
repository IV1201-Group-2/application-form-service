import pytest

from app.app import create_app, database


@pytest.fixture(scope='module')
def app_with_client():
    flask_app = create_app()
    flask_app.config.update({
        'TESTING': True,
        'JWT_SECRET_KEY': 'your-test-secret-key',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })

    with flask_app.app_context():
        database.create_all()
        database.session.commit()

    with flask_app.test_client() as testing_client:
        yield flask_app, testing_client

    with flask_app.app_context():
        database.session.remove()
        database.drop_all()
