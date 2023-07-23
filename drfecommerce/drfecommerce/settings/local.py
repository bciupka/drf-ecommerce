from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY_LOCAL')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}