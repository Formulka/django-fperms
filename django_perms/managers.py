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


class BasePermManager(models.Manager):

    perm_for = None

    def assign_perm(self, perm, perm_for, model=None, obj=None, field_name=None):
        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted("Object %s needs to be persisted first" % obj)

        perm = get_perm(perm, model, obj, field_name)

        obj_perm, _ = self.get_or_create(**{
            self.perm_for: perm_for,
            'perm': perm,
        })
        return obj_perm

    def remove_perm(self, perm, perm_for, model=None, obj=None, field_name=None):
        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted("Object %s needs to be persisted first" % obj)

        perm = get_perm(perm, model, obj, field_name)

        return self.filter(**{
            self.perm_for: perm_for,
            'perm': perm,
        }).delete()

    def get_all_perms(self, perm_for):
        from django_perms.models import Perm

        perm_pks = self.get_queryset().filter(**{
            self.perm_for: perm_for,
        }).values_list('perm__pk', flat=True)

        return Perm.objects.filter(pk__in=perm_pks)


class UserPermManager(BasePermManager):

    perm_for = 'user'


class GroupPermManager(BasePermManager):

    perm_for = 'group'
