from django.apps import apps
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from django_perms import get_perm_model
from django_perms.utils import get_content_type


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
        perm_obj = get_perm_from_permission_codename(perm)
        return user_obj.perms.has_perm(perm_obj, obj)

    def has_module_perms(self, user_obj, app_label):
        if not user_obj.is_active:
            return False

        ctypes = ContentType.objects.filter(app_label=app_label)

        return Perm.objects.filter(user_perms__user=user_obj, content_type__in=ctypes)

    def _get_user_permissions(self, user_obj):
        return user_obj.perms.all()

    def _get_group_permissions(self, user_obj):
        user_groups_field = get_user_model()._meta.get_field('groups')
        user_groups_query = 'group_perms__group__%s' % user_groups_field.related_query_name()

        return Perm.objects.filter(**{user_groups_query: user_obj})

    def _get_permissions(self, user_obj, obj, from_name):
        """
        Returns the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group" or "user" to return permissions from
        `_get_group_permissions` or `_get_user_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = '_perms_%s_perm_cache' % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Perm.objects.all()
            else:
                perms = getattr(self, '_get_%s_permissions' % from_name)(user_obj)
            setattr(user_obj, perm_cache_name, set(perm.perm_str for perm in perms))
        return getattr(user_obj, perm_cache_name)

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_perms_perm_cache'):
            user_obj._perms_perm_cache = self.get_user_permissions(user_obj)
            user_obj._perms_perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._perms_perm_cache
