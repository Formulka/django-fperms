from django.db import models

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
        from django_perms.models import Perm

        perm_pks = self.get_queryset().values_list('perm__pk', flat=True)
        return Perm.objects.filter(pk__in=perm_pks)

    def add(self, perm, obj=None):
        # add a permission to the related group or user
        print(perm, self.perm_holder, self.perm_holder_slug)
        obj_perm, _ = self.perm_model.objects.get_or_create(**{
            self.perm_holder_slug: self.perm_holder,
            'perm': get_perm(perm, obj),
        })
        return obj_perm

    def remove(self, perm, obj=None):
        # remove a permission from the related group or user

        return self.get_queryset().filter(perm=get_perm(perm, obj)).delete()

    def has_perm(self, perm, obj=None):
        from django_perms.models import Perm

        try:
            perm = get_perm(perm, obj)
        except Perm.DoesNotExist:
            return False

        return perm in self.all()
