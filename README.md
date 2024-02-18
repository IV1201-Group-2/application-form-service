# Application Form API

This API is used by applicants to submit their application for a job. The API allows applicants to check their
registered personal information as well as submit an application.

## Personal Info Endpoint

`GET /api/application-form/applicant/personal-info`

### Additional requirements

* The user must be logged in when calling this API
* The user's JWT token must be included in the `Authorization` header

### Successful response

The API returns an object with the following structure:

```json
{
  "id": 0,
  "first_name": "John",
  "last_name": "Doe",
  "email": "johndoe@example.com",
  "phone_number": "1234567890",
  "address": "123 Main St, Anytown, Anystate, 12345"
}
```

### Error responses

#### `USER_NOT_FOUND` (404 Not Found)

No user was found with the ID specified in the JWT token

#### `COULD_NOT_FETCH_USER` (500 Internal Server Error)

There was an issue with the database operation when trying to fetch the user's information

#### `UNAUTHORIZED` (401 Unauthorized)

User is not logged in (JWT token was not provided or is invalid)

#### `INVALID_TOKEN` (401 Unauthorized)

The provided JWT token is invalid (e.g., it is expired, not yet valid, or does not contain the required claims)

#### `TOKEN_NOT_PROVIDED` (401 Unauthorized)

No JWT token was provided in the `Authorization` header

#### `TOKEN_REVOKED` (401 Unauthorized)

The provided JWT token has been revoked

## Get Competences Endpoint

`GET /api/application-form/applicant/competences`

### Additional requirements

* The user must be logged in when calling this API
* The user's JWT token must be included in the `Authorization` header

### Successful response

The API returns a list of competences with the following structure:

```json
[
  {
    "competence_id": 0,
    "competence_name": "Python",
    "years_of_experience": 5
  },
  ...
]
```

### Error responses

#### `UNAUTHORIZED` (401 Unauthorized)

User is not logged in (JWT token was not provided or is invalid)

#### `INVALID_TOKEN` (401 Unauthorized)

The provided JWT token is invalid (e.g., it is expired, not yet valid, or does not contain the required claims)

#### `TOKEN_NOT_PROVIDED` (401 Unauthorized)

No JWT token was provided in the `Authorization` header

#### `TOKEN_REVOKED` (401 Unauthorized)

The provided JWT token has been revoked

## Add Submitted Application Endpoint

`POST /api/application-form/applicant/submit-application`

### Additional requirements

* The user must be logged in when calling this API
* The user's JWT token must be included in the `Authorization` header
* The request body must contain a JSON object with the following structure:

```json
{
  "competences": [
    {
      "competence_id": 0,
      "years_of_experience": 5
    },
    ...
  ],
  "availabilities": [
    {
      "from_date": "2023-01-01",
      "to_date": "2023-12-31"
    },
    ...
  ]
}
```

### Successful response

The API returns a JSON object with the following structure:

```json
{
  "status": "application_status",
  "competences": [
    {
      "competence_id": 0,
      "years_of_experience": 5
    },
    ...
  ],
  "availabilities": [
    {
      "from_date": "2023-01-01",
      "to_date": "2023-12-31"
    },
    ...
  ]
}
```

### Error responses

#### `INVALID_JSON_PAYLOAD` (400 Bad Request)

The request body is not a valid JSON object

#### `INVALID_PAYLOAD_STRUCTURE` (400 Bad Request)

The structure of the JSON object in the request body is invalid

#### `MISSING_COMPETENCE_ID` (400 Bad Request)

A competence in the request body does not have a `competence_id` key

#### `MISSING_YEARS_OF_EXPERIENCE` (400 Bad Request)

A competence in the request body does not have a `years_of_experience` key

#### `INVALID_COMPETENCE_ID` (400 Bad Request)

A competence in the request body has an invalid `competence_id` value

#### `INVALID_YEARS_OF_EXPERIENCE` (400 Bad Request)

A competence in the request body has an invalid `years_of_experience` value

#### `MISSING_AVAILABILITIES` (400 Bad Request)

The request body does not have an `availabilities` key

#### `INVALID_AVAILABILITY` (400 Bad Request)

An availability in the request body is not a valid JSON object

#### `MISSING_FROM_DATE` (400 Bad Request)

An availability in the request body does not have a `from_date` key

#### `MISSING_TO_DATE` (400 Bad Request)

An availability in the request body does not have a `to_date` key

#### `INVALID_DATE_FORMAT` (400 Bad Request)

An availability in the request body has an invalid date format

#### `INVALID_DATE_RANGE` (400 Bad Request)

An availability in the request body has an invalid date range

#### `UNAUTHORIZED` (401 Unauthorized)

User is not logged in (JWT token was not provided or is invalid)

#### `INVALID_TOKEN` (401 Unauthorized)

The provided JWT token is invalid (e.g., it is expired, not yet valid, or does not contain the required claims)

#### `TOKEN_NOT_PROVIDED` (401 Unauthorized)

No JWT token was provided in the `Authorization` header

#### `TOKEN_REVOKED` (401 Unauthorized)

The provided JWT token has been revoked

#### `INTERNAL_SERVER_ERROR` (500 Internal Server Error)

There was an issue with the database operation when trying to store the application

## Installation

This project uses pip for package management. The dependencies for the project are listed in the `requirements.txt`
and `requirements-dev.txt` files.

### Installing Dependencies

To install the dependencies for this project, follow the steps below:

1. Create a virtual environment (optional, but recommended):

```bash
python -m venv env
```

2. Activate the virtual environment:

On Windows:

```bash
env\Scripts\activate
```

On Unix or MacOS:

```bash
source env/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

### Installing Development Dependencies

If you plan to contribute to the project, you should also install the development dependencies. After activating your
virtual environment, run:

```bash
pip install -r requirements-dev.txt
```

## Deployment

The application is designed to be deployed on Heroku. You can follow the steps below to deploy the application:

1. Create a new Heroku application.
2. Set the `DATABASE_URL` environment variable in the Heroku application settings to your PostgreSQL database URL.
3. Push the application code to the Heroku application's Git repository.

## Database Configuration

The application uses PostgreSQL as its database. The database URL should be set in the `DATABASE_URL` environment
variable.

## Testing

Tests are written using pytest. You can run the tests by executing the following command in the root directory of the
project:

```bash
pytest
```

## Linting

Flake8 is used for linting the code. You can run the linter by executing the following command in the root directory of
the project:

```bash
flake8 --show-source app tests
```

## Static Analysis

Mypy is used for static type checking. You can run the static type checker by executing the following command in the
root directory of the project:

```bash
mypy app tests
```