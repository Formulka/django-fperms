from django.contrib.contenttypes.models import ContentType
from fperms.conf import settings

from fperms import get_perm_model, enums


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
        if settings.PERM_AUTO_CREATE:
            # create the required perm if it doesn't exist and is supposed to be created
            perm = perm_model.objects.create(**perm_kwargs)
        else:
            # check if a wildcard permission exists instead
            perm_kwargs['codename'] = enums.PERM_CODENAME_WILDCARD
            perm = perm_model.objects.get(**perm_kwargs)

    return perm
