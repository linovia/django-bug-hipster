import django
from django.conf import settings
from bughipster import settings as base_settings


def pytest_configure(config):
    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3',
                    'TEST_NAME': ':memory:',
                },
            },
            INSTALLED_APPS=base_settings.INSTALLED_APPS,
            ROOT_URLCONF=base_settings.ROOT_URLCONF,
            DEBUG=False,
            SITE_ID=1,
            TEMPLATE_DEBUG=False,
            ALLOWED_HOSTS=['*'],
            STATIC_URL='/static/',
        )
        django.setup()
