from django.contrib.contenttypes.models import ContentType

from fperms import get_perm_model, enums


def is_obj_persisted(obj):
    return getattr(obj, 'pk', None) is not None


def get_content_type(obj):
    return ContentType.objects.get_for_model(obj)


def get_perm(perm, obj=None):
    perm_model = get_perm_model()

    if isinstance(perm, perm_model):
        return perm

    perm_kwargs = perm_model.get_perm_kwargs(perm, obj)

    try:
        perm = perm_model.objects.get(**perm_kwargs)
    except perm_model.DoesNotExist:
        # check if a wildcard permission exists instead
        perm_kwargs['codename'] = enums.PERM_CODENAME_WILDCARD
        perm = perm_model.objects.get(**perm_kwargs)

    return perm
