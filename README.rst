=============================
django-fperms
=============================

.. image:: https://badge.fury.io/py/django-fperms.svg
    :target: https://badge.fury.io/py/django-fperms

.. image:: https://travis-ci.org/Formulka/django-fperms.svg?branch=master
    :target: https://travis-ci.org/Formulka/django-fperms

.. image:: https://codecov.io/gh/Formulka/django-fperms/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Formulka/django-fperms

Flexible Django permissions backend

Documentation
-------------

The full documentation is at https://django-fperms.readthedocs.io.

Quickstart
----------

Install django-fperms::

    pip install django-fperms

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'fperms.apps.FPermsConfig',
        ...
    )

Add django-fperms's URL patterns:

.. code-block:: python

    from fperms import urls as fperms_urls


    urlpatterns = [
        ...
        url(r'^', include(fperms_urls)),
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
