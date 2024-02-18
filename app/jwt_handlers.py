from flask import current_app, jsonify
from flask_jwt_extended import JWTManager
from jwt import InvalidTokenError


def register_jwt_handlers(jwt: JWTManager) -> None:
    """
    Register JWT error handlers for handling token-related issues.

    This function registers error handlers for JWT tokens. These handlers
    handle invalid tokens, expired tokens, and unauthorized requests.

    :param jwt: The Flask JWTManager instance.
    :returns: None
    """

    @jwt.invalid_token_loader
    def invalid_token_callback(error: InvalidTokenError) -> tuple:
        """
        Callback for handling invalid JWT tokens.

        This function handles invalid JWT tokens by logging the error and
        returning a JSON response with an 'INVALID_TOKEN' message and a 401
        status code.

        :param error: The InvalidTokenError object.
        :returns: A tuple containing a JSON response and a status code.
        """

        current_app.logger.warning(f'Invalid JWT provided: {error}')
        return jsonify({'error': 'INVALID_TOKEN', }), 401

    @jwt.expired_token_loader
    def expired_token_callback(header: dict, payload: dict) -> tuple:
        """
        Callback for handling expired JWT tokens.

        This function handles expired JWT tokens by logging the error and
        returning a JSON response with a 'TOKEN_EXPIRED' message and a 401
        status code.

        :param header: The JWT header.
        :param payload: The JWT payload.
        :returns: A tuple containing a JSON response and a status code.
        """

        current_app.logger.warning('Expired JWT token')
        return jsonify({'error': 'TOKEN_EXPIRED'}), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error: str) -> tuple:
        """
        Callback for handling unauthorized requests.

        This function handles unauthorized requests by logging the error and
        returning a JSON response with an 'UNAUTHORIZED' message and a 401
        status code.

        :param error: A description of the unauthorized request.
        :returns: A tuple containing a JSON response and a status code.
        """

        current_app.logger.warning(f'Unauthorized request: {error}')
        return jsonify({'error': 'UNAUTHORIZED'}), 401
