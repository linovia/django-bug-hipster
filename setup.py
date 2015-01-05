"""
setup
~~~~~

:copyright: (c) 2014 by ,
see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


install_requires = [
    'Django<1.8',
    'psycopg2',
    # 'logan==0.5.9.1',
    'django-crispy-forms==1.4.0',
    'django-filter==0.9.1',
]


tests_require = [
    'pytest',
    'pytest-cov>=1.4',
    'pytest-django',
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='bughipster',
    version='0.1.0',
    author='Xavier Ordoquy',
    author_email='xordoquy@linovia.com',

    url='https://github.com/linovia/bughipster',
    description='',
    long_description=open('README.md').read(),
    license='BSD',

    packages=[
        'bughipster',
    ],
    package_dir={'bughipster': 'bughipster'},
    zip_safe=False,

    install_requires=install_requires,
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'bughipster = bughipster.runner:main',
        ],
    },

    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],

    cmdclass={'test': PyTest},
    tests_require=tests_require,
    extras_require={
        'tests': tests_require,
    },
)
