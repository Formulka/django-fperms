from django.contrib.contenttypes.models import ContentType


def is_obj_persisted(obj):
    return getattr(obj, 'pk', None) is None


def get_content_type(obj):
    ContentType.objects.get_for_model(obj)


def get_permission(perm, ctype, obj=None, field_name=None):
    from django_perms.models import BasePerm, Perm, GlobalPerm, ObjectPerm, FieldPerm

    if not issubclass(perm, BasePerm):
        if field_name is not None:
            model = FieldPerm
        elif obj is not None:
            model = ObjectPerm
        elif ctype == GlobalPerm:
            model = GlobalPerm
        else:
            model = Perm
        return model.objects.get(content_type=ctype, codename=perm)
    else:
        return perm
