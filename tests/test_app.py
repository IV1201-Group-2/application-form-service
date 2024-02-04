import os


def test_app_initialization(app_with_client):
    app, _ = app_with_client
    assert app is not None
    assert app.config['TESTING'] is True
    assert app.config['JWT_SECRET_KEY'] == 'your-test-secret-key'
    assert 'sqlite:///:memory:' in app.config['SQLALCHEMY_DATABASE_URI']


def test_logging_setup(app_with_client):
    app, _ = app_with_client
    log_dir = app.config.get('LOG_DIR')
    assert os.path.exists(log_dir)


def test_extensions_setup(app_with_client):
    app, _ = app_with_client
    assert 'sqlalchemy' in app.extensions
    assert 'flask-jwt-extended' in app.extensions


def test_blueprint_registration(app_with_client):
    app, _ = app_with_client
    blueprints = [bp.name for bp in app.blueprints.values()]
    assert 'personal_info' in blueprints
