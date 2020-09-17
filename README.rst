=============================
django-fperms
=============================

.. image:: https://badge.fury.io/py/django-fperms.svg
    :target: https://badge.fury.io/py/django-fperms

.. image:: https://travis-ci.org/Formulka/django-fperms.svg?branch=master
    :target: https://travis-ci.org/druids/django-fperms

.. image:: https://codecov.io/gh/Formulka/django-fperms/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/druids/django-fperms

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


Out of the box you have access to several new permission types:

- **generic**: for general purpose project wide permissions
- **model**: for per model permissions (similar to django default permissions)
- **instance**: for per instance permissions, similar to model permissions but specific per instance
- **field**: for per model field permissions, similar to model permissions but specific per model field, work in progress

You can also create your own permission model subclassing the abstract base permission class:

.. code-block:: python

    fperms.models.BasePerm

and setting the ``PERM_MODEL`` variable in your project settings with the path to your custom model. E.g.

.. code-block:: python

    ...
    PERM_MODEL='fperms.models.Perm'
    ...

You can find an example of custom permission model at https://github.com/formulka/django-fperms-iscore

Usage
-----

A superuser has for all intents and purposes permission to do everything. For regular users you can assign permissions directly or via a user group.

**Creating a new permission**:

You can create a new permission directly via its model or via a specially formated string:

.. code-block:: python

    from fperms import enums
    from fperms.models import Perm

    Perm.objects.create(
        type=enums.PERM_TYPE_GENERIC,
        codename='export',
    )
    Perm.objects.create_from_str('generic.export')

**Assigning a permission**:

You can assign existing permission via the custom ``perms`` manager available for both User (including custom ones) and Group models. You can add single permission or multiple both directly via its instance or using the formated string:

.. code-block:: python

    from django.auth.models import User, Group

    from fperms.models import Perm

    perm_export = Perm.objects.create(
        type=enums.PERM_TYPE_GENERIC,
        codename='export',
    )
    perm_import = Perm.objects.create(
        type=enums.PERM_TYPE_GENERIC,
        codename='import',
    )

    user = User.objects.get(pk=1)
    user.fperms.add_perm(perm_export)
    user.fperms.add_perm(perms=[perm_export, perm_import])

    group = Group.objects.get(pk=1)
    group.fperms.add_perm(perms=['generic.export', 'generic.import'])

By default if said permission does not exist, it will raise an exception. You can override this behavior by setting ``PERM_AUTO_CREATE`` variable in your project settings to ``True``, assigning a permission will then create it as well if it does not exist.

**Retrieving permission instance**:

You can get a permission instance directly from the model or via the string representation.

.. code-block:: python

    perm = Perm.objects.get(type=enums.PERM_TYPE_GENERIC, codename='export')
    perm = Perm.objects.get_from_str('generic.export')

**Checking permission**:

You can check whether the user or group has a required permission via ``has_perm`` method of the ``perms`` manager again using both the permission instance or the string representation.

.. code-block:: python

    ...
    perm = Perm.objects.create(
        type=enums.PERM_TYPE_GENERIC,
        codename='export',
    )

    assert user.fperms.has_perm(perm)
    assert user.fperms.has_perm('generic.export')

Built in perm types
-------------------

**generic**

- generic permission useful for project wide permissions
- type is defined as ``fperms.enums.PERM_TYPE_GENERIC``, it is the default permission type
- it requires ``type`` and ``codename`` fields (type being default only the codename is actually required)
- string representation is ``'generic.<codename>'``

.. code-block:: python

    ...
    # equivalent results:
    Perm.objects.create(
        codename='export',
    )
    Perm.objects.create_from_str('generic.export')

**model**

- model level permission analogous to the builtin django permissions
- type is defined as ``fperms.enums.PERM_TYPE_MODEL``
- it requires ``type``, ``content_type`` and ``codename`` fields
- django admin is using codenames ``add``, ``change`` and ``delete`` for its inner workings
- string representation is ``'model.<app_label>.<module_name>.<codename>'``

.. code-block:: python

    from fperms import enums
    from fprems.utils import get_content_type
    ...
    # equivalent results:
    Perm.objects.create(
        type=enums.PERM_TYPE_MODEL,
        content_type=get_content_type(Article),
        codename='add',
    )
    Perm.objects.create_from_str('model.articles.Article.add')

**object**

- model level permission specific per object
- type is defined as ``fperms.enums.PERM_TYPE_OBJECT``
- it requires ``type``, ``content_type``, ``object_id`` and ``codename`` fields
- django admin is using codenames ``add``, ``change`` and ``delete`` for its inner workings
- string representation is ``'object.<app_label>.<module_name>.<codename>'``

.. code-block:: python

    from fperms import enums
    from fprems.utils import get_content_type
    ...
    article = Article.objects.get(pk=1)
    # equivalent results:
    Perm.objects.create(
        type=enums.PERM_TYPE_OBJECT,
        content_type=get_content_type(Article),
        object_id=article.pk,
        codename='add',
    )
    Perm.objects.create_from_str('object.articles.Article.add', obj_id=article.pk)

    # creating multiple permissions for a single object at once is supported
    Perm.objects.create_from_str(perms=[
                                    'object.articles.Article.add',
                                    'object.articles.Article.change',
                                    'object.articles.Article.delete',
                                ], obj_id=article.pk)

**field**

- model level permission specific per model field
- type is defined as ``fperms.enums.PERM_TYPE_FIELD``
- it requires ``type``, ``content_type``, ``name`` and ``codename`` fields
- string representation is ``'field.<app_label>.<module_name>.<name>.<codename>'``
- TODO:  this permission type is not fully implemented yet

.. code-block:: python

    from fperms import enums
    from fprems.utils import get_content_type
    ...
    article = Article.objects.get(pk=1)
    # equivalent results:
    Perm.objects.create(
        type=enums.PERM_TYPE_FIELD,
        content_type=get_content_type(Article),
        name='name',
        codename='add',
    )
    Perm.objects.create_from_str('field.articles.Article.name.add')

Admin
-----

Flexible permisssions support django admin interface, to enable them you need to first update the list of authentication backends in your project settings:

.. code-block:: python

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'fperms.backends.PermBackend',
    ]

and then simply subclass the ``fperms.admin.PermModelAdmin`` instead of the regular ``admin.ModelAdmin``:

.. code-block:: python

    from django.contrib import admin
    from fperms.admin import PermModelAdmin

    from articles.models import Article


    @admin.register(Article)
    class ArticleAdmin(PermModelAdmin):
        pass

To enable per-instance permission support, set ``perms_per_instance`` property of the admin class to ``True``.

.. code-block:: python

    ...
    @admin.register(Article)
    class ArticleAdmin(PermModelAdmin):

        perms_per_instance = True

User still needs model level permission for each model it should be able to access via admin site.

If the ``perms_per_instance`` option is set to ``True``, author of a new instance will automatically receive the permission to update and delete said instance.
You can override this behavior by setting ``perms_per_instance_author_change`` and ``perms_per_instance_author_delete`` admin properties respectively to ``False``.

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
