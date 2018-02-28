from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.utils.functional import cached_property

from django_perms.models import Perm
from django_perms.utils import get_content_type, get_perm_kwargs


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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if self.model._meta.perms_per_instance and self.model._meta.perms_per_instance_auto_author:
            perm, _ = Perm.objects.get_or_create(
                content_type=get_content_type(self.model),
                object_id=obj.pk,
                codename='change',
            )
            request.user.perms.add(perm)

    def has_perm(self, user, codename=None, obj=None):
        object_id = obj.pk if obj is not None else None
        try:
            perm = self._perms.get(codename=codename, object_id=object_id)
        except Perm.DoesNotExist:
            perm = None

        return user.perms.has_perm(perm) or user.is_superuser if perm is not None else False

    def has_add_permission(self, request):
        return self.has_perm(request.user, 'add')

    def has_change_permission(self, request, obj=None):
        if self.model._meta.perms_per_instance:
            return self.has_perm(request.user, 'change', obj=obj)

        return self.has_perm(request.user, 'change')

    def has_delete_permission(self, request, obj=None):
        if self.model._meta.perms_per_instance:
            return self.has_perm(request.user, 'delete', obj=obj)

        return self.has_perm(request.user, 'delete')

    def has_module_permission(self, request):
        return self._perms.filter(userperms__user=request.user)

    def get_changelist(self, request, **kwargs):
        return PermChangeList
