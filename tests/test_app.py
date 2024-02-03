import os
import unittest

from app.app import create_app


class TestConfigLoaded(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_config_loaded(self):
        self.assertIsNotNone(self.app.config.get('JWT_SECRET_KEY'))
        self.assertIsNotNone(self.app.config.get('SQLALCHEMY_DATABASE_URI'))
        self.assertIsNotNone(self.app.config.get('LOG_LEVEL'))
        self.assertIsNotNone(self.app.config.get('LOG_FORMAT'))
        self.assertIsNotNone(self.app.config.get('LOG_DIR'))
        self.assertIsNotNone(self.app.config.get('LOG_FILENAME'))
        self.assertIsNotNone(self.app.config.get('LOG_FILE'))
        self.assertIsNotNone(self.app.config.get('LOG_TO_STDOUT'))


class TestLogging(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_log_file_created(self):
        self.app.logger.info("Test log message")
        self.assertTrue(os.path.exists(self.app.config.get('LOG_FILE')))

    def test_log_file_has_correct_format(self):
        self.client.get('/applicant/personal_info')
        expected_log_format = \
            r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - \w+\.?\w* - \w+ - .*'
        with open(self.app.config.get('LOG_FILE'), 'r') as log_file:
            log_file_content = log_file.read()
            self.assertRegex(log_file_content, expected_log_format)

    def test_log_file_has_correct_level(self):
        with open(self.app.config.get('LOG_FILE'), 'r') as log_file:
            log_file_content = log_file.read()
            self.assertIn(self.app.config.get('LOG_LEVEL'), log_file_content)

    def test_log_file_has_correct_filename(self):
        log_path = self.app.config.get('LOG_FILE')
        log_filename = os.path.basename(log_path)
        self.assertEqual(log_filename, self.app.config.get('LOG_FILENAME'))
