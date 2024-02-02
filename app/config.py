import os

JWT_SECRET_KEY = os.environ.get('JWT_SECRET')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')

LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DIR = os.environ.get('LOG_DIR', 'logs')
LOG_FILENAME = os.environ.get('LOG_FILENAME', 'app.log')
LOG_FILE = os.path.join(LOG_DIR, LOG_FILENAME)

if 'DYNO' in os.environ:
    LOG_TO_STDOUT = True
else:
    LOG_TO_STDOUT = False
