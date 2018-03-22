=============================
django-fperms
=============================

.. image:: https://badge.fury.io/py/django-fperms.svg
    :target: https://badge.fury.io/py/django-fperms

.. image:: https://travis-ci.org/Formulka/django-fperms.svg?branch=master
    :target: https://travis-ci.org/Formulka/django-fperms

.. image:: https://codecov.io/gh/Formulka/django-fperms/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Formulka/django-fperms

The flexible permissions library uses a custom permission model, that when installed patches itself into the standard django authentication library.

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


Settings
--------

Out of the box you have access to several new permission types:

- **generic**: for general purpose project wide permissions
- **model**: for per model permissions (similar to django default permissions)
- **instance**: for per instance permissions, similar to model permissions but specific per instance
- **field**: for per model field permissions, similar to model permissions but specific per model field, work in progress

You can also create your own permission model subclassing the abstract base permission class:

.. code-block:: python

    fperms.models.BasePerm

and setting the `PERM_MODEL` variable in your project settings with the path to your custom model. E.g.

.. code-block:: python

    ...
    PERM_MODEL='fperms.models.Perm'
    ...

You can find an example of custom permission model at https://github.com/formulka/django-fperms-iscore

Admin
-----

Flexible permisssions support django admin interface, to enable them you need to update the list of authentication backends in your project settings:

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'fperms.backends.PermBackend',
    ]

and then simply subclass the `fperms.admin.PermModelAdmin` instead of the regular `admin.ModelAdmin`

.. code-block:: python

    from django.contrib import admin
    from fperms.admin import PermModelAdmin

    from articles.models import Article


    @admin.register(Article)
    class ArticleAdmin(PermModelAdmin):
        pass

To enable per-instance permission support, set `perms_per_instance` property of the admin class to `True`.

.. code-block:: python

    ...
    @admin.register(Article)
    class ArticleAdmin(PermModelAdmin):
        
        perms_per_instance = True

User still needs model level permission for each model it should be able to access via admin site.

If the `perms_per_instance` option is set to `True`, author of a new instance will automatically receive the permission to update and delete said instance. 
You can override this behavior by setting `perms_per_instance_author_change` and `perms_per_instance_author_delete` admin properties respectively to `False`.


Usage
-----

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
