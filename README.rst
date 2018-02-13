=============================
django-perms
=============================

.. image:: https://badge.fury.io/py/django-perms.svg
    :target: https://badge.fury.io/py/django-perms

.. image:: https://travis-ci.org/formulka/django-perms.svg?branch=master
    :target: https://travis-ci.org/formulka/django-perms

.. image:: https://codecov.io/gh/formulka/django-perms/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/formulka/django-perms

Flexible Django permissions backend

Documentation
-------------

The full documentation is at https://django-perms.readthedocs.io.

Quickstart
----------

Install django-perms::

    pip install django-perms

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_perms.apps.DjangoPermsConfig',
        ...
    )

Add django-perms's URL patterns:

.. code-block:: python

    from django_perms import urls as django_perms_urls


    urlpatterns = [
        ...
        url(r'^', include(django_perms_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
