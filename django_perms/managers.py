from functools import partialmethod

from django.db import models

from django_perms import get_perm_model, enums
from django_perms.utils import get_perm


PERM_USER_SLUG = 'user'
PERM_GROUP_SLUG = 'group'


class PermManagerMetaclass(type):

    def __new__(mcs, name, bases, attrs):
        # adds magical helper methods to the perm manager to filter specified perm type
        new_class = super().__new__(mcs, name, bases, attrs)
        for perm_type in enums.PERM_TYPE_CHOICES:
            setattr(new_class, '%s_perms' % perm_type[0],
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


class PermRelatedManager:
    # Fake perms manager for group and user

    perm_model = None
    perm_holder = None
    perm_holder_slug = None

    def __init__(self, perm_holder, perm_model):
        self.perm_model = perm_model
        self.perm_holder = perm_holder
        self.perm_holder_slug = perm_model.perm_holder_slug

    def get_queryset(self):
        return self.perm_model.objects.filter(**{
            self.perm_holder_slug: self.perm_holder,
        })

    def all(self):
        # get all permissions for related group or user
        all_perm_cache_name = 'all_perm_cache'
        if not hasattr(self, all_perm_cache_name):
            perm_pks = set(self.get_queryset().values_list('perm__pk', flat=True))

            # If the related object is a user, add permissions from its groups
            if self.perm_holder_slug == PERM_USER_SLUG:
                for group in self.perm_holder.groups.all():
                    perm_pks.update(set(group.perms.all().values_list('pk', flat=True)))

            setattr(self, all_perm_cache_name, get_perm_model().objects.filter(pk__in=perm_pks))
        return getattr(self, all_perm_cache_name)

    def _add(self, perm, obj):
        # add a permission to the related group or user
        obj_perm, _ = self.perm_model.objects.get_or_create(**{
            self.perm_holder_slug: self.perm_holder,
            'perm': get_perm(perm, obj),
        })
        return obj_perm

    def add(self, perms, obj=None):
        if isinstance(perms, str) or isinstance(perms, get_perm_model()):
            perms = [perms]

        obj_perms = []
        for perm in perms:
            obj_perms.append(self._add(perm, obj))

        return obj_perms

    def remove(self, perm, obj=None):
        # remove a permission from the related group or user
        return self.get_perm(perm, obj=obj).remove()

    def clear(self):
        # remove all permissions from the related group or user
        self.all().remove()

    def get_perm(self, perm, obj=None):
        # get a permission if it belongs to group or user
        perm = get_perm(perm, obj)

        return self.all().get(pk=perm.pk)

    def has_perm(self, perm, obj=None):
        # determine whether a user or a group has provided permission
        try:
            self.get_perm(perm, obj)
        except get_perm_model().DoesNotExist:
            return False

        return True
