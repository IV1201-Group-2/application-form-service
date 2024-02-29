import logging

from flask import jsonify, request
from werkzeug.exceptions import HTTPException

from app.utilities.status_codes import StatusCodes


def handle_all_unhandled_exceptions(exception):
    """
    Handle all unhandled exceptions.

    This function handles all unhandled exceptions by logging the exception and
    returning an appropriate JSON response with a status code.

    :param exception: The unhandled exception.
    :returns: A tuple containing a JSON response and a status code.
    """

    requester_ip = request.remote_addr

    if isinstance(exception, HTTPException) and 'favicon.ico' in request.url:
        logging.warning(f'{requester_ip} - Favicon not found')
        return jsonify({'error': 'NOT_FOUND'}), StatusCodes.NOT_FOUND

    if (isinstance(exception, HTTPException) and
            exception.code == StatusCodes.NOT_FOUND):
        logging.error(f'{requester_ip} - URL not found: {request.url}')
        return jsonify({'error': 'NOT_FOUND'}), StatusCodes.NOT_FOUND

    logging.critical(f'{requester_ip} - ' + str(exception))
    return (jsonify({'error': 'INTERNAL_SERVER_ERROR'}),
            StatusCodes.INTERNAL_SERVER_ERROR)
