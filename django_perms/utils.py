from django.contrib.contenttypes.models import ContentType


def is_obj_persisted(obj):
    return getattr(obj, 'pk', None) is not None


def get_content_type(obj):
    return ContentType.objects.get_for_model(obj)


def get_perm(perm, model=None, obj=None, field_name=None):
    from django_perms.models import Perm

    content_type = get_content_type(model or obj) if model or obj else None

    if not isinstance(perm, Perm):
        perm = Perm.objects.get(
            codename=perm,
            content_type=content_type,
            object_id=obj.pk if obj else None,
            field_name=field_name
        )

    return perm
