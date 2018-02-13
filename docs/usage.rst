=====
Usage
=====

To use django-perms in a project, add it to your `INSTALLED_APPS`:

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
