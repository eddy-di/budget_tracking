from .base import *


DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'budget_tracker',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        "HOST": "localhost",
        "PORT": "5432",
    }
}


SITE_URL = 'https://mysite.com:8000/' 