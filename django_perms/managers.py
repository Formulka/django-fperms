from django.db import models
from django_perms.utils import get_perm


class PermManager(models.Manager):

    def model_perms(self):
        return self.get_queryset().filter(
            content_type__isnull=False,
            object_id__isnull=True,
            field_name__isnull=True,
        )

    def object_perms(self):
        return self.get_queryset().filter(
            content_type__isnull=False,
            object_id__isnull=False,
            field_name__isnull=True,
        )

    def field_perms(self):
        return self.get_queryset().filter(
            content_type__isnull=False,
            field_name__isnull=False,
            object_id__isnull=True,
        )

    def generic_perms(self):
        return self.get_queryset().filter(
            content_type__isnull=True,
            field_name__isnull=True,
            object_id__isnull=True,
        )


class BasePermRelatedManager:
    # Fake perms manager for group and user

    perm_for = None
    perm_for_model = None
    perm_for_slug = None

    def __init__(self, perm_for_model, perm_for):
        self.perm_for_model = perm_for_model
        self.perm_for = perm_for

    def get_queryset(self):
        return self.perm_for_model.objects.all()

    def all(self):
        # Get all permissions for related group or user

        from django_perms.models import Perm

        perm_pks = self.get_queryset().filter(**{
            self.perm_for_slug: self.perm_for,
        }).values_list('perm__pk', flat=True)

        return Perm.objects.filter(pk__in=perm_pks)

    def add(self, perm, obj=None):
        # add a permission to the related group or user

        obj_perm, _ = self.perm_for_model.objects.get_or_create(**{
            self.perm_for_slug: self.perm_for,
            'perm': get_perm(perm, obj),
        })
        return obj_perm

    def remove(self, perm, obj=None):
        # remove a permission from the related group or user

        return self.get_queryset().filter(**{
            self.perm_for_slug: self.perm_for,
            'perm': get_perm(perm, obj),
        }).delete()

    def has_perm(self, perm, obj=None):
        from django_perms.models import Perm

        try:
            get_perm(perm, obj)
        except Perm.DoesNotExist:
            return False

        return True


class UserPermManagerMixin:
    perm_for_slug = 'user'


class GroupPermManagerMixin:
    perm_for_slug = 'group'


class UserPermRelatedManager(UserPermManagerMixin, BasePermRelatedManager):
    pass


class GroupPermRelatedManager(GroupPermManagerMixin, BasePermRelatedManager):
    pass
