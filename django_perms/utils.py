from django.contrib.contenttypes.models import ContentType


def is_obj_persisted(obj):
    return getattr(obj, 'pk', None) is not None


def get_content_type(obj):
    from django_perms.models import GlobalPerm

    # if the obj in question is None, assume it is a global permission
    return ContentType.objects.get_for_model(obj) if obj is not None else GlobalPerm


def get_perm(perm, model=None, obj=None, field_name=None):
    from django_perms.models import Perm, GlobalPerm, ObjectPerm, FieldPerm

    ctype = get_content_type(model or obj)

    if not isinstance(perm, Perm):
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
