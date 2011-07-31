DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dash',
        'USER': 'pyrun',
        'PASSWORD': 'ajfhkdsrypqwe',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CELERY_RESULT_DBURI = "%(ENGINE)s://%(USER)s:%(PASSWORD)s@%(HOST)s/%(NAME)s" % DATABASES['default']
CELERY_ALWAYS_EAGER = False
CELERYD_CONCURRENCY = 2
