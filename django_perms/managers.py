from django.db import models

from django_perms import get_perm_model
from django_perms.utils import get_perm, get_perm_kwargs


class PermManager(models.Manager):

    def perm_exists(self, perm, obj=None):
        try:
            get_perm(perm, obj)
        except self.DoesNotExist:
            return False
        return True

    def get_from_str(self, perm, obj=None):
        perm_kwargs = get_perm_kwargs(perm, obj)
        return self.get(**perm_kwargs)

    def create_from_str(self, perm, obj=None):
        perm_kwargs = get_perm_kwargs(perm, obj)
        return self.create(**perm_kwargs)


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
        # Get all permissions for related group or user
        perm_pks = self.get_queryset().values_list('perm__pk', flat=True)
        return get_perm_model().objects.filter(pk__in=perm_pks)

    def add(self, perm, obj=None):
        # add a permission to the related group or user
        obj_perm, _ = self.perm_model.objects.get_or_create(**{
            self.perm_holder_slug: self.perm_holder,
            'perm': get_perm(perm, obj),
        })
        return obj_perm

    def remove(self, perm, obj=None):
        # remove a permission from the related group or user

        return self.get_queryset().filter(perm=get_perm(perm, obj)).delete()

    def has_perm(self, perm, obj=None):
        try:
            perm = get_perm(perm, obj)
        except get_perm_model().DoesNotExist:
            return False

        return perm in self.all()
