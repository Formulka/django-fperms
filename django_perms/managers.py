from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_perms.exceptions import ObjectNotPersisted, IncorrectContentType, IncorrectObject
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

    def add(self, perm, model=None, obj=None, field_name=None):
        # add a permission to the related group or user

        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted(_('Object %s needs to be persisted first') % obj)

        perm = get_perm(perm, model, obj, field_name)

        obj_perm, _ = self.perm_for_model.objects.get_or_create(**{
            self.perm_for_slug: self.perm_for,
            'perm': perm,
        })
        return obj_perm

    def remove(self, perm, model=None, obj=None, field_name=None):
        # remove a permission from the related group or user

        if obj is not None and not is_obj_persisted(obj):
            raise ObjectNotPersisted(_('Object %s needs to be persisted first') % obj)

        perm = get_perm(perm, model, obj, field_name)

        return self.get_queryset().filter(**{
            self.perm_for_slug: self.perm_for,
            'perm': perm,
        }).delete()

    def has_perm(self, perm, obj=None):
        from django_perms.models import PERM_TYPE_GENERIC, PERM_TYPE_MODEL, PERM_TYPE_OBJECT, PERM_TYPE_FIELD

        perm_type, perm_arg_string = perm.split('.', 1)

        codename = content_type = object_id = field_name = None

        if perm_type == PERM_TYPE_GENERIC:
            codename = perm_arg_string
        elif perm_type == PERM_TYPE_MODEL:
            model_name, codename = perm_arg_string.rsplit('.', 1)
            model = apps.get_model(model_name)
            content_type = ContentType.objects.get_for_model(model)
        elif perm_type == PERM_TYPE_OBJECT:
            model_name, codename = perm_arg_string.rsplit('.', 1)
            model = apps.get_model(model_name)
            content_type = ContentType.objects.get_for_model(model)

            if not isinstance(obj, models.Model):
                raise IncorrectObject(_('Object %s must be a model instance') % obj)
            if not isinstance(obj, model):
                raise IncorrectContentType(_('Object %s does not have a correct content type') % obj)
            if not is_obj_persisted(obj):
                raise ObjectNotPersisted(_('Object %s needs to be persisted first') % obj)

            object_id = obj.pk
        elif perm_type == PERM_TYPE_FIELD:
            model_name, field_name, codename = perm_arg_string.rsplit('.', 2)
            model = apps.get_model(model_name)
            content_type = ContentType.objects.get_for_model(model)

        return self.all().filter(
            codename=codename,
            content_type=content_type,
            object_id=object_id,
            field_name=field_name,
        ).exists()


class UserPermManagerMixin:

    perm_for_slug = 'user'


class GroupPermManagerMixin:

    perm_for_slug = 'group'


class UserPermRelatedManager(UserPermManagerMixin, BasePermRelatedManager):
    pass


class GroupPermRelatedManager(GroupPermManagerMixin, BasePermRelatedManager):
    pass
