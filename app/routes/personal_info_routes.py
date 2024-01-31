from flask import Blueprint, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.personal_info_service import fetch_personal_info

personal_info_bp = Blueprint('personal_info', __name__)


@personal_info_bp.route('/get', methods=['GET'])
@jwt_required()
def get_personal_info() -> tuple[Response, int]:
    current_user = get_jwt_identity()
    personal_info = fetch_personal_info(current_user)
    if personal_info is None:
        return jsonify({'error': 'No personal info found for username.'}), 404

    return jsonify(personal_info), 200
