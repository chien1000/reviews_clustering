from .base import *

SECRET_KEY = ')&9pdh0p##h6s3m7f06=70)wrtkr!izhl#vrsai!z2xriz+(6x'
DEBUG = True


# database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}
