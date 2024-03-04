# Application Form Service
This API is used by applicants to submit their application for a job. It is a microservice that is part of a recruitment application.
## General Information
- **Programming Language**: Python
- **Virtual Environment**: Python venv
- **Framework**: Flask
- **Application Modularity**: Flask Blueprints 
- **API Design**: RESTful principles
- **Configuration Management**: Externalized to config.py
- **Security**: Flask-JWT-Extended (authentication & authorization)
- **CORS**: Flask-Cors
- **Logging**: Flask-Logging + Root Logger
- **Database Integration**: Flask-SQLAlchemy
- **Database**: PostgreSQL
- **Testing**: Pytest + Testcontainers
- **Code Coverage**: pytest-cov
- **Linting**: flake8
- **Dependency Management**: Pip
- **Continuous Integration**: GitHub Actions
- **Continuous Deployment**: Heroku

## Project Setup
Ensure all commands are executed from the project root.

1. **Environment Setup**: Create and activate a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install Dependencies**: Install all required dependencies.
    ```bash
    pip install -r requirements.txt
    ```

3. **Run Tests**: Execute all tests (requires Docker to run locally).
    ```bash
    pytest
    ```

4. **Code Coverage**: Generate code coverage report (requires Docker to run locally).
    ```bash
    pytest --cov=app
    ```

5. **Linting**: Run linting checks.
    ```bash
   flake8 --show-source --statistics app tests
    ```

6. **Environment Variables**:
   - Setup as specified in config.py.


7. **Run Development Server**: Start the development server.
    ```bash
    flask --app app/app run
    ```

8. **Run Heroku Locally**: Run the application locally using Heroku.
    ```bash
    heroku local
    ```

## Directory Structure

```
📦 
├─ .github
│  └─ workflows      - Contains GitHub Actions workflow files.
├─ app
│  ├─ models         - Contains database entities.
│  ├─ repositories   - Handles database interactions.
│  ├─ routes         - Defines application routes.
│  ├─ services       - Implements business logic.
│  └─ utilities      - Contains HTTP status codes.
└─ tests
   ├─ repositories   - Unit tests for repository functions.
   ├─ routes         - Unit tests for route handlers.
   ├─ services       - Unit tests for service layer functions.
   └─ utilities      - Utility functions for testing.
```