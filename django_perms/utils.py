from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_perms import get_perm_model, enums
from django_perms.exceptions import ObjectNotPersisted, IncorrectContentType, IncorrectObject


def is_obj_persisted(obj):
    return getattr(obj, 'pk', None) is not None


def get_content_type(obj):
    return ContentType.objects.get_for_model(obj)


def get_perm_kwargs(perm, obj=None):
    perm_type, perm_arg_string = perm.split('.', 1)

    model = content_type = object_id = field_name = None

    if perm_type == enums.PERM_TYPE_MODEL or perm_type == enums.PERM_TYPE_OBJECT:
        model_name, codename = perm_arg_string.rsplit('.', 1)
        model = apps.get_model(model_name)
        if perm_type == enums.PERM_TYPE_OBJECT:
            if not isinstance(obj, models.Model):
                raise IncorrectObject(_('Object %s must be a model instance') % obj)
            if not isinstance(obj, model):
                raise IncorrectContentType(_('Object %s does not have a correct content type') % obj)
            if not is_obj_persisted(obj):
                raise ObjectNotPersisted(_('Object %s needs to be persisted first') % obj)

            object_id = obj.pk
    elif perm_type == enums.PERM_TYPE_FIELD:
        model_name, field_name, codename = perm_arg_string.rsplit('.', 2)
        model = apps.get_model(model_name)
    else:
        codename = perm_arg_string

    if model:
        content_type = ContentType.objects.get_for_model(model)

    return dict(
        codename=codename,
        content_type=content_type,
        object_id=object_id,
        field_name=field_name,
    )


def get_perm(perm, obj=None):
    perm_model = get_perm_model()

    if isinstance(perm, perm_model):
        return perm

    perm_kwargs = get_perm_kwargs(perm, obj)

    try:
        perm = perm_model.objects.get(**perm_kwargs)
    except perm_model.DoesNotExist:
        # check if a wildcard permission exists instead
        perm_kwargs['codename'] = enums.PERM_CODENAME_WILDCARD
        perm = perm_model.objects.get(**perm_kwargs)

    return perm
