from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from django_perms.models import Perm
from django_perms.utils import get_content_type


def get_perm_from_permission_codename(permission_codename):
    app_label, model_action = permission_codename.split('.', 1)
    action, model_name = model_action.split('_')
    model = apps.get_model(app_label, model_name)

    return Perm.objects.get(
        content_type=get_content_type(model),
        codename=action,
        object_id=None,
        field_name=None,
    )


class PermBackend(ModelBackend):

    def has_perm(self, user_obj, perm, obj=None):
        perm_obj = get_perm_from_permission_codename(perm)
        return user_obj.perms.has_perm(perm_obj, obj)
