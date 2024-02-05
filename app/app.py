import logging
import os

from flask import Flask

from app import jwt_handlers
from app.extensions import database, jwt
from app.routes.applicant.personal_info_routes import personal_info_bp
from app.routes.competences_routes import competences_bp


def create_app() -> Flask:
    """
    Creates and configures the Flask application.

    :return: The configured Flask application.
    """

    application_form_api = Flask(__name__)
    application_form_api.config.from_pyfile('config.py')

    setup_logging(application_form_api)
    setup_extensions(application_form_api)
    register_blueprints(application_form_api)

    return application_form_api


def setup_logging(application_form_api: Flask) -> None:
    """
    Sets up logging for the Flask application.

    :param application_form_api: The Flask application.
    """

    log_dir = application_form_api.config.get('LOG_DIR', 'logs')
    os.makedirs(
            log_dir, exist_ok=True)

    logging.basicConfig(
            level=application_form_api.config.get('LOG_LEVEL', logging.INFO),
            format=application_form_api.config.get(
                    'LOG_FORMAT',
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            filename=application_form_api.config.get(
                    'LOG_FILE', os.path.join(log_dir, 'app.log'))
    )


def setup_extensions(application_form_api: Flask) -> None:
    """
    Sets up extensions for the Flask application.

    :param application_form_api: The Flask application.
    """

    database.init_app(application_form_api)
    jwt.init_app(application_form_api)
    jwt_handlers.register_jwt_handlers(jwt)


def register_blueprints(application_form_api: Flask) -> None:
    """
    Registers blueprints for the Flask application.

    :param application_form_api: The Flask application.
    """

    application_form_api.register_blueprint(
            personal_info_bp,
            url_prefix='/application-form/applicant/personal_info')
    application_form_api.register_blueprint(
            competences_bp, url_prefix='/application-form/competences')


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
