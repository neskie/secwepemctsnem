# Django settings for secwepemctsnem project.
import os
from local_settings import *

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__)

STATIC_DOC_ROOT = os.path.join(PROJECT_ROOT, '/media/')

ADMINS = (
    ('Neskie Manuel', 'neskiem@gmail.com'),
)
MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'radio',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'email@gmail.com'
EMAIL_HOST_PASSWORD = 'emailpassword'
SECRET_KEY = 'thisisasecret'
