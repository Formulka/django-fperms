from __future__ import unicode_literals
from django.db import models
from django_perms.exceptions import ObjectNotPersisted
from django_perms.utils import is_obj_persisted, get_perm


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

    def global_perms(self):
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

    def add(self, perm, model=None, obj=None, field_name=None):
        # add a permission to the related group or user

        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted("Object %s needs to be persisted first" % obj)

        perm = get_perm(perm, model, obj, field_name)

        obj_perm, _ = self.perm_for_model.objects.get_or_create(**{
            self.perm_for_slug: self.perm_for,
            'perm': perm,
        })
        return obj_perm

    def remove(self, perm, model=None, obj=None, field_name=None):
        # remove a permission from the related group or user

        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted("Object %s needs to be persisted first" % obj)

        perm = get_perm(perm, model, obj, field_name)

        return self.get_queryset().filter(**{
            self.perm_for_slug: self.perm_for,
            'perm': perm,
        }).delete()


class UserPermManagerMixin:

    perm_for_slug = 'user'


class GroupPermManagerMixin:

    perm_for_slug = 'group'


class UserPermRelatedManager(UserPermManagerMixin, BasePermRelatedManager):
    pass


class GroupPermRelatedManager(UserPermManagerMixin, BasePermRelatedManager):
    pass
