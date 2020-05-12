import os


class BaseConfig:
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    CORS_ORIGIN_WHITELIST = ['http://localhost:5000']
    DB_USER = "emmanuel"
    DB_PASSWORD = "root"
    DB_NAME = "test_server_db"
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}'


class DevelopmentConfig(BaseConfig):
    # DEVELOPMENT = True
    # SQLALCHEMY_DATABASE_URI = 'mysql://christ:u08NCWmOuWdiD93b@localhost:3306/test_server_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USER = "emmanuel"
    DB_PASSWORD = "root"
    DB_NAME = "test_server_db"
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}'
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    TESTING = False
    # MAIL_USERNAME = ''
    # MAIL_PASSWORD = ''
    # MAIL_DEFAULT_SENDER = ''


class TestingConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USER = ""
    DB_PASSWORD = ""
    DB_NAME = ""
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    TESTING = True


# class Config(object):
# DEBUG = False
# BCRYPT_LOG_ROUNDS = 13
# TESTING = False
# CSRF_ENABLED = True
# SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
# FLASK_SERVER_NAME = 'localhost:8000'
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SWAGGER_UI_DOC_EXPANSION = 'list'
# RESTPLUS_VALIDATE = True
# RESTPLUS_MASK_SWAGGER = False
# ERROR_404_HELP = False
# MAIL_SERVER = 'smtp.googlemail.com'
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD')
# MAIL_DEFAULT_SENDER = 'from@example.com'

# TEST_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'

# class ProductionConfig(Config):
# DEBUG = False
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# PAYLOAD_EXPIRATION_TIME = 3000

# class StagingConfig(Config):
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# DEVELOPMENT = True
# DEBUG = True
# PAYLOAD_EXPIRATION_TIME = 3000

# class DevelopmentConfig(Config):
# DEVELOPMENT = True
# DEBUG = True
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# PAYLOAD_EXPIRATION_TIME = 3000

# class TestingConfig(Config):
# TESTING = True
# SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
# PRESERVE_CONTEXT_ON_EXCEPTION = False
# BCRYPT_LOG_ROUNDS = 4
# PAYLOAD_EXPIRATION_TIME = 5
