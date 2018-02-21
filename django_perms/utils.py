from django.contrib.contenttypes.models import ContentType

from django_perms.models import BasePermission


def is_obj_persisted(obj):
    return getattr(obj, 'pk', None) is None


def get_content_type(obj):
    ContentType.objects.get_for_model(obj)


def get_permission(perm, ctype):
    if not isinstance(perm, BasePermission):
        return BasePermission.objects.get(content_type=ctype, codename=perm)
    else:
        return perm
