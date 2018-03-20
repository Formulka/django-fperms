=====
Usage
=====

To use django-fperms in a project, add it to your `INSTALLED_APPS`:

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
