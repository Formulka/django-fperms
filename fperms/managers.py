import operator

from functools import partialmethod, reduce

from django.db import models
from django.db.models import Q

from fperms import get_perm_model, enums
from fperms.conf import settings
from fperms.utils import get_perm


PERM_USER_SLUG = 'users'
PERM_GROUP_SLUG = 'fgroups'


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

    def _get_all_group_fperms(self, group):
        perm_pks = set(group.fperms.all().values_list('pk', flat=True))
        for subgroup in group.fgroups.all():
            perm_pks.update(self._get_all_group_fperms(subgroup))
        return perm_pks

    def all_perms(self):
        if self.query_field_name == PERM_USER_SLUG:
            q_list = [Q(users=self.instance), Q(fgroups__users=self.instance)]
            for i in range(1, settings.PERM_GROUP_MAX_LEVEL + 1):
                q_list.append(Q(**{'fgroups__{}__users'.format('__'.join(i * ['parents'])): self.instance}))
        else:
            q_list = [Q(fgroups=self.instance)]
            for i in range(1, settings.PERM_GROUP_MAX_LEVEL + 1):
                q_list.append(Q(**{'fgroups__{}'.format('__'.join(i * ['parents'])): self.instance}))

        return self.model.objects.filter(
            pk__in=self.model.objects.filter(reduce(operator.or_, q_list)).values('pk')
        )

    def get_perms(self, *perms, obj=None):
        obj_perms = []
        for perm in perms:
            obj_perms.append(get_perm(perm, obj))
        return obj_perms

    def add_perm(self, *perms, obj=None):
        return self.add(*self.get_perms(*perms, obj=obj))

    def remove_perm(self, *perms, obj=None):
        return self.remove(*self.get_perms(*perms, obj=obj))

    def has_perm(self, perm, obj=None):
        # determine whether a user or a group has provided permission
        if hasattr(self.instance, 'is_superuser') and self.instance.is_superuser:
            return True

        perm = get_perm(perm, obj)
        if perm is None:
            return False
        else:
            return self.all_perms().filter(pk=get_perm(perm, obj).pk).exists()
