from __future__ import unicode_literals
from django.db import models
from django_perms.exceptions import ObjectNotPersisted
from django_perms.utils import is_obj_persisted, get_content_type, get_permission


class BasePermissionManager(models.Manager):

    perm_for = None

    def assign_perm(self, perm, perm_for, obj=None, field_name=None):
        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted("Object %s needs to be persisted first" % obj)

        ctype = get_content_type(obj)
        permission = get_permission(perm, ctype, obj, field_name)

        obj_perm, _ = self.get_or_create(**{
            self.perm_for: perm_for,
            'permission': permission,
            'content_type': ctype,
            'content_object': obj
        })
        return obj_perm

    def remove_perm(self, perm, perm_for, obj=None, field_name=None):
        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted("Object %s needs to be persisted first" % obj)

        ctype = get_content_type(obj)
        permission = get_permission(perm, ctype, obj, field_name)

        return self.filter(**{
            self.perm_for: perm_for,
            'permission': permission,
            'content_type': ctype,
            'content_object': obj
        }).delete()


class UserPermissionManager(BasePermissionManager):

    perm_for = 'user'


class GroupPermissionManager(BasePermissionManager):

    perm_for = 'group'
