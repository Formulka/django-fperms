from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.utils.functional import cached_property

from django_perms.models import Perm
from django_perms.utils import get_content_type


class PermAdminMixin:

    @cached_property
    def _perms(self):
        return Perm.objects.filter(content_type=get_content_type(self.model))


class PermChangeList(PermAdminMixin, ChangeList):

    def get_queryset(self, request):
        object_ids = self._perms.filter(object_id__isnull=False, codename='change').values_list('object_id', flat=True)

        qs = super().get_queryset(request)
        return qs.filter(pk__in=object_ids)


class PermAdmin(PermAdminMixin, ModelAdmin):

    perms_per_instance = False
    perms_per_instance_author_change = True
    perms_per_instance_author_delete = True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # add the change and delete permissions for the author of a new model instance
        if not change and self.perms_per_instance:
            for codename in ('change', 'delete'):
                if hasattr(self, 'perms_per_instance_author_'+codename):
                    self.add_perm(request.user, codename, obj)

    def get_changelist(self, request, **kwargs):
        return PermChangeList

    def has_change_permission(self, request, obj=None):
        if self.perms_per_instance:
            return self.has_perm(request.user, 'change', obj=obj)

        return self.has_perm(request.user, 'change')

    def has_delete_permission(self, request, obj=None):
        if self.perms_per_instance:
            return self.has_perm(request.user, 'delete', obj=obj)

        return self.has_perm(request.user, 'delete')

    def add_perm(self, user, codename, obj):
        object_id = obj.pk if obj is not None else None
        perm_kwargs = {
            'content_type': get_content_type(self.model),
            'object_id': object_id,
        }

        perm, _ = Perm.objects.get_or_create(codename=codename, **perm_kwargs)
        user.perms.add(perm)

    def has_perm(self, user, codename=None, obj=None):
        object_id = obj.pk if obj is not None else None
        try:
            perm = self._perms.get(codename=codename, object_id=object_id)
            return user.perms.has_perm(perm)
        except Perm.DoesNotExist:
            return False
