class StatusCodes:
    """
    Represents the HTTP status codes that can be returned by the API.

    :ivar OK: The request was successful.
    :ivar CREATED: The resource was created successfully.
    :ivar BAD_REQUEST: The request was malformed.
    :ivar UNAUTHORIZED: The request was unauthorized.
    :ivar NOT_FOUND: The resource was not found.
    :ivar CONFLICT: The request could not be completed due to a conflict.
    :ivar INTERNAL_SERVER_ERROR: An internal server error occurred.
    """

    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500
