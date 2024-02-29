import logging
import os

from flask import Flask
from flask_cors import CORS

from app import jwt_handlers
from app.extensions import database, jwt
from app.routes.application_route import application_submission_bp
from app.routes.competences_route import competences_bp
from app.routes.error_handler import handle_all_unhandled_exceptions


def create_app() -> Flask:
    """
    Creates and configures the Flask application.

    This function creates a new Flask application, configures it from a
    configuration file, sets up CORS, logging, extensions, and registers
    blueprints. Also sets up a global error handler for unhandled exceptions.

    :returns: The configured Flask application.
    """

    application_form_api = Flask(__name__)
    application_form_api.config.from_pyfile('config.py')
    application_form_api.errorhandler(Exception)(
            handle_all_unhandled_exceptions)

    CORS(application_form_api, resources={r"/api/*": {
        "origins": "https://client-service-f45dc8e85ddf.herokuapp.com"}})

    setup_logging(application_form_api)
    setup_extensions(application_form_api)
    register_blueprints(application_form_api)

    return application_form_api


def setup_logging(application_form_api: Flask) -> None:
    """
    Sets up logging for the Flask application.

    This function sets up logging for the Flask application. If LOG_TO_STDOUT
    is enabled in the configuration, it sets up logging to stdout. Otherwise,
    it configures logging to a file.

    :param application_form_api: The Flask application.
    """

    log_level = application_form_api.config.get('LOG_LEVEL', 'INFO').upper()
    log_format = application_form_api.config.get(
            'LOG_FORMAT',
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if application_form_api.config.get('LOG_TO_STDOUT'):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(stream_handler)
    else:
        log_dir = application_form_api.config.get('LOG_DIR', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(application_form_api.config.get(
                'LOG_FILE', os.path.join(log_dir, 'app.log')))
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)

    logging.getLogger().setLevel(log_level)


def setup_extensions(application_form_api: Flask) -> None:
    """
    Sets up extensions for the Flask application.

    This function initializes the database and JWT extensions for the Flask
    application, and registers JWT error handlers. It also creates all
    database tables.

    :param application_form_api: The Flask application.
    """

    database.init_app(application_form_api)
    jwt.init_app(application_form_api)
    jwt_handlers.register_jwt_handlers(jwt)

    with application_form_api.app_context():
        database.create_all()


def register_blueprints(application_form_api: Flask) -> None:
    """
    Registers blueprints for the Flask application.

    This function registers blueprints for the Flask application. Each
    blueprint corresponds to a different part of the application.

    :param application_form_api: The Flask application.
    """

    application_form_api.register_blueprint(
            competences_bp,
            url_prefix='/api/application-form/competences')
    application_form_api.register_blueprint(
            application_submission_bp,
            url_prefix='/api/application-form/submit')


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

application = create_app()
