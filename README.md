django-bug-hipster
==================

https://travis-ci.org/linovia/django-bug-hipster.svg?branch=master

Bugzilla rewritten with Django.


Installation
------------

> We recommand you use a virtual environment to install the project. See 
> https://virtualenv.pypa.io/en/latest/

To install the project:

    $ pip install -r requirements.txt

Update the bughipster/settings.py file to setup the database. At the moment it
will only work with an existing Bugzilla database.

    $ python manage.py runserver
