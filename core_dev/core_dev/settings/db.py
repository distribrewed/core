import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DB_HOST', 'postgres'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'NAME': os.environ.get('DB_NAME', 'distribrewed'),
        'USER': os.environ.get('DB_USER', 'distribrewed'),
        'PASSWORD': os.environ.get('DB_PASS', 'secretpass'),
    }
}