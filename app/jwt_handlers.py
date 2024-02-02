from flask import jsonify, current_app
from flask_jwt_extended import JWTManager
from jwt import InvalidTokenError


def register_jwt_handlers(jwt: JWTManager) -> None:
    @jwt.invalid_token_loader
    def invalid_token_callback(error: InvalidTokenError) -> tuple:
        current_app.logger.warning(f'Invalid JWT provided: {error}')
        return jsonify({
            'error': 'Invalid token provided',
            'details': str(error)
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(header: dict, payload: dict) -> tuple:
        current_app.logger.warning('Expired JWT token')
        return jsonify({
            'error': 'Token has expired',
            'details': 'The token has expired. Please log in again.'
        }), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error: str) -> tuple:
        current_app.logger.warning(f'Unauthorized request: {error}')
        return jsonify({
            'error': 'Unauthorized',
            'details': str(error)
        }), 401
