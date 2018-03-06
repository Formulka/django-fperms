from functools import partialmethod

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import ModelBase
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from django_perms import enums
from django_perms.conf import settings as perm_settings
from django_perms.managers import PermManager, PermRelatedManager


class PermMetaclass(ModelBase):

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)
        for perm_type in enums.PERM_TYPE_CHOICES:
            setattr(new_class, 'is_%s_perm' % perm_type[0],
                    partialmethod(new_class.is_TYPE_perm, perm_type=perm_type[0]))

        return new_class


class BasePerm(models.Model, metaclass=PermMetaclass):

    type = models.CharField(
        max_length=10,
        choices=enums.PERM_TYPE_CHOICES,
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
    object_id = models.SmallIntegerField(
        _('object pk'),
        null=True,
        blank=True,
    )
    content_object = GenericForeignKey()
    field_name = models.CharField(
        _('field name'),
        max_length=100,
        null=True,
        blank=True,
    )

    objects = PermManager()

    class Meta:
        abstract = True
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        ordering = ('content_type', 'object_id', 'field_name', 'codename',)
        unique_together = (
            ('type', 'codename', 'content_type', 'object_id', 'field_name'),
        )

    def __str__(self):
        if self.name:
            return self.name

        permission_name = str(enums.PERM_CODENAMES.get(self.codename, _('Permission')))
        name = getattr(self, '_%s_perm_name' % self.type, '')

        return ' | '.join(('Permission', name, permission_name))

    @cached_property
    def model(self):
        return self.content_type.model_class()

    @cached_property
    def perm_str(self):
        perm_str_args = [
            self.type,
        ] + getattr(self, '_%s_perm_str', [])

        return '.'.join(perm_str_args)

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
        return _('model %s') % (
            self.model.__name__
        )

    @property
    def _object_perm_name(self):
        return _('model %s | object %s') % (
            self.model.__name__,
            self.content_object,
        )

    @property
    def _field_perm_name(self):
        return _('model %s | field %s') % (
            self.model.__name__,
            self.model._meta.get_field(self.field_name).verbose_name,
        )

    @property
    def _model_perm_str_args(self):
        return [
            self.type,
            self.content_type.app_label,
            self.content_type.model,
            self.codename,
        ]

    @property
    def _object_perm_str_args(self):
        return [
            self.type,
            self.content_type.app_label,
            self.content_type.model,
            str(self.object_id),
            self.codename,
        ]

    @property
    def _field_perm_str_args(self):
        return [
            self.type,
            self.content_type.app_label,
            self.content_type.model,
            self.field_name,
            self.codename,
        ]

    @property
    def _generic_perm_str_args(self):
        return []


class Perm(BasePerm):
    pass


class UserPerm(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_perms',
    )
    perm = models.ForeignKey(
        perm_settings.PERM_MODEL,
        on_delete=models.CASCADE,
        related_name='user_perms',
    )

    perm_holder_slug = 'user'

    class Meta:
        verbose_name = _('user perm')
        verbose_name_plural = _('user perms')
        ordering = ('user',)
        unique_together = (
            ('user', 'perm'),
        )

    def __str__(self):
        return '%s | %s' % (
            self.user,
            self.perm
        )


class GroupPerm(models.Model):

    group = models.ForeignKey(Group, related_name='group_perms')
    perm = models.ForeignKey(perm_settings.PERM_MODEL, on_delete=models.CASCADE, related_name='group_perms')

    perm_holder_slug = 'group'

    class Meta:
        verbose_name = _('group perm')
        verbose_name_plural = _('group perms')
        ordering = ('group',)
        unique_together = (
            ('group', 'perm'),
        )

    def __str__(self):
        return '%s | %s' % (
            self.group,
            self.perm
        )


def monkey_patch_user():
    user_model = get_user_model()
    setattr(user_model, 'perms', property(lambda self: PermRelatedManager(self, UserPerm)))


def monkey_patch_group():
    setattr(Group, 'perms', property(lambda self: PermRelatedManager(self, GroupPerm)))


monkey_patch_user()
monkey_patch_group()
