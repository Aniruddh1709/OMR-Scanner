# Statement for enabling the development environment
DEBUG = True


import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

secret_key = "blahblahblah"
# SQLALCHEMY_DATABASE_URI = '??????'
# DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2


CSRF_ENABLED     = True


CSRF_SESSION_KEY = "secret"


SECRET_KEY = "secret"