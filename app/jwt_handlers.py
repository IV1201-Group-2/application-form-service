from flask import current_app, jsonify
from flask_jwt_extended import JWTManager
from jwt import InvalidTokenError


def register_jwt_handlers(jwt: JWTManager) -> None:
    """Register JWT error handlers for handling token-related issues.

    :param jwt: The Flask JWTManager instance.
    :returns: None
    """

    @jwt.invalid_token_loader
    def invalid_token_callback(error: InvalidTokenError) -> tuple:
        """Callback for handling invalid JWT tokens.

        :param error: The InvalidTokenError object.
        :returns: A tuple containing a JSON response and
        HTTP status code (401 Unauthorized).
        """

        current_app.logger.warning(f'Invalid JWT provided: {error}')
        return jsonify({
            'error': 'INVALID_TOKEN',
            'details': 'Invalid token provided'
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(header: dict, payload: dict) -> tuple:
        """Callback for handling expired JWT tokens.

        :param header: The JWT header.
        :param payload: The JWT payload. :returns: A tuple containing a JSON
        response and HTTP status code (401 Unauthorized).
        """

        current_app.logger.warning('Expired JWT token')
        return jsonify({
            'error': 'TOKEN_EXPIRED',
            'details': 'The token has expired. Please log in again.'
        }), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error: str) -> tuple:
        """Callback for handling unauthorized requests.

        :param error: A description of the unauthorized request.
        :returns: A tuple containing a JSON response and
        HTTP status code (401 Unauthorized).
        """

        current_app.logger.warning(f'Unauthorized request: {error}')
        return jsonify({
            'error': 'UNAUTHORIZED',
            'details': 'Unauthorized request. Please log in.'
        }), 401
