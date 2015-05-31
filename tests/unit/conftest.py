import django
from django.conf import settings
from bughipster import settings as base_settings


def pytest_configure(config):
    if not settings.configured:
        test_settings = base_settings.__dict__
        test_settings.update({
            'DATABASES': {
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3',
                    'TEST_NAME': ':memory:',
                },
            },
        })
        settings.configure(**test_settings)
        django.setup()
