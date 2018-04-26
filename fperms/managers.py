from functools import partialmethod

from django.db import models

from fperms import get_perm_model, enums
from fperms.utils import get_perm


PERM_USER_SLUG = 'users'
PERM_GROUP_SLUG = 'groups'


class PermManagerMetaclass(type):

    def __new__(mcs, name, bases, attrs):
        # adds magical helper methods to the perm manager to filter specified perm type
        new_class = super().__new__(mcs, name, bases, attrs)
        for perm_type in enums.PERM_TYPE_CHOICES:
            setattr(new_class, '{}_perms'.format(perm_type[0]),
                    partialmethod(new_class.TYPE_perms, perm_type=perm_type[0]))

        return new_class


class PermManager(models.Manager, metaclass=PermManagerMetaclass):

    def perm_exists(self, perm, obj=None):
        # determine whether a permission exists
        try:
            get_perm(perm, obj)
        except self.DoesNotExist:
            return False
        return True

    def get_from_str(self, perm, obj=None):
        # get a perm instance based on perm kwargs
        perm_kwargs = get_perm_model().get_perm_kwargs(perm, obj)
        return self.get(**perm_kwargs)

    def _create_from_str(self, perm, obj):
        # create a perm instance based on perm kwargs
        perm_kwargs = get_perm_model().get_perm_kwargs(perm, obj)
        return self.create(**perm_kwargs)

    def create_from_str(self, perms, obj=None):
        if isinstance(perms, str):
            perms = [perms]

        obj_perms = []
        for perm in perms:
            obj_perms.append(self._create_from_str(perm, obj))
        return obj_perms

    def TYPE_perms(self, perm_type):
        # return all perms of the specified type
        # used to generate magical helper methods in the metaclass
        return self.get_queryset().filter(perm_type=perm_type)


class RelatedPermManager(models.Manager):

    def all_perms(self):
        # get all permissions for related group or user
        all_perms_cache_name = 'all_perms_cache'
        if not hasattr(self, all_perms_cache_name):
            perm_pks = set(self.all().values_list('pk', flat=True))
            # If the related object is a user, add permissions from its groups
            if self.query_field_name == PERM_USER_SLUG:
                for group in self.instance.groups.all():
                    perm_pks.update(set(group.perms.all().values_list('pk', flat=True)))

            setattr(self, all_perms_cache_name, self.model.objects.filter(pk__in=perm_pks))
        return getattr(self, all_perms_cache_name)

    def get_perms(self, *perms, obj=None):
        obj_perms = []
        for perm in perms:
            obj_perms.append(get_perm(perm, obj))
        return obj_perms

    def add_perm(self, *perms, obj=None):
        return self.add(*self.get_perms(*perms, obj=obj))

    def remove_perm(self, *perms, obj=None):
        return self.remove(*self.get_perms(*perms, obj=obj))

    def get_perm(self, perm, obj=None):
        # get a permission if it belongs to group or user
        perm = get_perm(perm, obj)

        return self.all_perms().get(pk=perm.pk)

    def has_perm(self, perm, obj=None):
        # determine whether a user or a group has provided permission
        if hasattr(self.instance, 'is_superuser') and self.instance.is_superuser:
            return True

        if perm is None:
            return False
        try:
            self.get_perm(perm, obj)
        except get_perm_model().DoesNotExist:
            return False

        return True
