from __future__ import unicode_literals
from django.db import models
from django_perms.exceptions import ObjectNotPersisted
from django_perms.utils import is_obj_persisted, get_content_type, get_perm


class BasePermissionManager(models.Manager):

    perm_for = None

    def assign_perm(self, perm, perm_for, model=None, obj=None, field_name=None):
        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted("Object %s needs to be persisted first" % obj)

        permission = get_perm(perm, model, obj, field_name)

        obj_perm, _ = self.get_or_create(**{
            self.perm_for: perm_for,
            'permission': permission,
        })
        return obj_perm

    def remove_perm(self, perm, perm_for, model=None, obj=None, field_name=None):
        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted("Object %s needs to be persisted first" % obj)

        permission = get_perm(perm, model, obj, field_name)

        return self.filter(**{
            self.perm_for: perm_for,
            'permission': permission,
        }).delete()


class UserPermissionManager(BasePermissionManager):

    perm_for = 'user'


class GroupPermissionManager(BasePermissionManager):

    perm_for = 'group'
