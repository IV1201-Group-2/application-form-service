import os

JWT_SECRET_KEY = os.environ.get('JWT_SECRET')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
