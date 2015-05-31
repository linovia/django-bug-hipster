django-bug-hipster
==================

[![Build Status](https://travis-ci.org/linovia/django-bug-hipster.svg?branch=master)](https://travis-ci.org/linovia/django-bug-hipster)
Bugzilla rewritten with Django.


Disclaimer
----------

This project's goal is to fully emulate Bugzilla. This means the user interface
will be the same but the arguments and overall behaviour.

Please do NOT USE this project as a reference for good pratices for what is
usually done with Django. This is NOT the case and totally out of prupose here.


Installation
------------

> We recommand you use a virtual environment to install the project. See 
> https://virtualenv.pypa.io/en/latest/

> Please note that you should use this project against an existing Bugzilla database.

To install the project:

    $ pip install .

Update the bughipster/settings.py file to setup the database. At the moment it
will only work with an existing Bugzilla database.

    $ python manage.py runserver
