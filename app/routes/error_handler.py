from flask import current_app, jsonify


def handle_all_unhandled_exceptions(exception):
    """
    Handle all unhandled exceptions.

    This function handles all unhandled exceptions by logging the exception and
    returning a JSON response with an 'INTERNAL_SERVER_ERROR' message and a 500
    status code.

    :param exception: The unhandled exception.
    :returns: A tuple containing a JSON response and a status code.
    """

    current_app.logger.error(exception)
    return jsonify({'error': 'INTERNAL_SERVER_ERROR'}), 500
