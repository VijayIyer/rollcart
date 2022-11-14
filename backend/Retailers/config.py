"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    DATABASE_PARAMS = {
        'USER_NAME':environ.get('DATABASE_USER_NAME'),
        'PASSWORD':environ.get('DATABASE_PASSWORD'),
        'SERVER_NAME':environ.get('DATABASE_SERVER_NAME'),
        'PORT_NUMBER':environ.get('DATABASE_PORT_NUMBER'),
        'NAME':environ.get('DATABASE_NAME')
    }
    WALMART_PARAMS = {
        'API_KEY':environ.get('WALMART_API_KEY'),
        'DEVICE':environ.get('WALMART_DEVICE'),
        'ENGINE':environ.get('WALMART_ENGINE')
    }
    TARGET_PARAMS = {
        'RAPIDAPI_KEY':environ.get('TARGET_RAPIDAPI_KEY'),
        'RAPIDAPI_HOST':environ.get('TARGET_RAPIDAPI_HOST'),
        'RAPIDAPI_PRODUCTNAME_HOST':environ.get('TARGET_RAPIDAPI_PRODUCTNAME_HOST')
    }
    KROGER_PARAMS = {
        'BASE_URL':environ.get('KROGER_BASE_URL'),
        'STORESEARCH_URL':environ.get('KROGER_STORESEARCH_URL'),
        'PRODUCTSEARCH_URL':environ.get('KROGER_PRODUCTSEARCH_URL'),
        'AUTH_TOKEN':environ.get('KROGER_AUTH_TOKEN')
    }
    WALGREENS_PARAMS = {
        'BASE_URL':environ.get('WALGREENS_BASE_URL'),
        'STORESEARCH_URL':environ.get('WALGREENS_STORESEARCH_URL'),
        'PRODUCTSEARCH_URL':environ.get('WALGREENS_PRODUCTSEARCH_URL'),
        'DEFAULT_RADIUS':environ.get('WALGREENS_DEFAULT_RADIUS'),
        'IN_STOCK_STRING':environ.get('WALGREENS_IN_STOCK_STRING')
    }


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True