DEBUG = False
ALLOWED_HOSTS = ['*'] # или ип адрес нашего сервера

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db1',
        'USER': 'django_shop',
        'PASSWORD': '01031988ss-20',
        'HOST': 'localhost',
        'PORT': '',  # SET to empty string for default.
    }
}