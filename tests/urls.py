from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from fperms.urls import urlpatterns as django_perms_urls

urlpatterns = [
    url(r'^', include(django_perms_urls, namespace='fperms')),
]
