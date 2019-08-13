from django.apps import apps
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from fperms import get_perm_model
from fperms.utils import get_content_type


Perm = get_perm_model()


def get_perm_from_permission_codename(permission_codename):
    # get permission object based on django hard-coded permission codename
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

    # authentication backend, mostly for compatibility with django admin site

    def has_perm(self, user_obj, perm, obj=None):
        if user_obj.is_superuser:
            return True
        try:
            perm_obj = get_perm_from_permission_codename(perm)
        except Perm.DoesNotExist:
            perm_obj = None
        return user_obj.perms.has_perm(perm_obj, obj)

    def has_module_perms(self, user_obj, app_label):
        if not user_obj.is_active:
            return False

        ctypes = ContentType.objects.filter(app_label=app_label)

        return Perm.objects.filter(users=user_obj, content_type__in=ctypes)
