from functools import partialmethod

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import ModelBase
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from fperms import enums
from fperms.exceptions import ObjectNotPersisted, IncorrectContentType, IncorrectObject
from fperms.managers import PermManager, RelatedPermManager


class PermMetaclass(ModelBase):

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)
        for perm_type in new_class.PERM_TYPE_CHOICES:
            setattr(new_class, 'is_{}_perm'.format(perm_type[0]),
                    partialmethod(new_class.is_TYPE_perm, perm_type=perm_type[0]))

        return new_class


class BasePerm(models.Model, metaclass=PermMetaclass):

    PERM_TYPE_CHOICES = enums.PERM_TYPE_CHOICES
    PERM_CODENAMES = enums.PERM_CODENAMES

    type = models.CharField(
        max_length=10,
        choices=PERM_TYPE_CHOICES,
        default=enums.PERM_TYPE_GENERIC,
    )
    codename = models.CharField(
        _('codename'),
        max_length=100,
    )
    name = models.CharField(
        _('name'),
        max_length=255,
        null=True,
        blank=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('content type'),
        blank=True,
        null=True,
    )
    object_id = models.TextField(
        _('object pk'),
        null=True,
        blank=True,
    )
    content_object = GenericForeignKey()
    groups = models.ManyToManyField(
        Group,
        related_name='perms',
        blank=True
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='perms',
        blank=True
    )

    objects = PermManager()

    class Meta:
        abstract = True
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        ordering = ('codename',)
        unique_together = (
            ('type', 'codename', 'content_type', 'object_id', 'field_name'),
        )

    def __str__(self):
        if self.name:
            return self.name

        permission_name = str(self.PERM_CODENAMES.get(self.codename, self.codename))
        name = getattr(self, '_{}_perm_name'.format(self.type), '')

        return ' | '.join(('Permission', name, permission_name))

    @cached_property
    def model(self):
        return self.content_type.model_class()

    @classmethod
    def get_perm_kwargs(cls, perm, obj=None):
        perm_type, perm_arg_string = perm.split('.', 1)

        model = content_type = object_id = field_name = None

        if perm_type == enums.PERM_TYPE_MODEL or perm_type == enums.PERM_TYPE_OBJECT:
            model_name, codename = perm_arg_string.rsplit('.', 1)
            model = apps.get_model(model_name)
            if perm_type == enums.PERM_TYPE_OBJECT:
                if not isinstance(obj, models.Model):
                    raise IncorrectObject(_('Object {} must be a model instance').format(obj))
                if not isinstance(obj, model):
                    raise IncorrectContentType(_('Object {} does not have a correct content type').format(obj))
                if obj.pk is None:
                    raise ObjectNotPersisted(_('Object {} needs to be persisted first').format(obj))

                object_id = obj.pk
        elif perm_type == enums.PERM_TYPE_FIELD:
            model_name, field_name, codename = perm_arg_string.rsplit('.', 2)
            model = apps.get_model(model_name)
        else:
            codename = perm_arg_string

        if model:
            content_type = ContentType.objects.get_for_model(model)

        return dict(
            type=perm_type,
            codename=codename,
            content_type=content_type,
            object_id=object_id,
            field_name=field_name,
        )

    def get_wildcard_perm(self):
        return self.objects.filter(
            type=self.type,
            codename=enums.PERM_CODENAME_WILDCARD,
            content_type=self.content_type,
            object_id=self.object_id,
            field_name=self.field_name,
        )

    def is_TYPE_perm(self, perm_type):
        return self.type == perm_type

    @property
    def _model_perm_name(self):
        return _('model {}').format(
            self.model.__name__
        )

    @property
    def _object_perm_name(self):
        return _('model {} | object {}') % (
            self.model.__name__,
            self.content_object,
        )

    @property
    def _field_perm_name(self):
        return _('model {} | field {}') % (
            self.model.__name__,
            self.model._meta.get_field(self.field_name).verbose_name,
        )
