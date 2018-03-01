from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import EMPTY_VALUES
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from django_perms.conf import settings as perm_settings
from django_perms.managers import (
    PermManager, UserPermRelatedManager, GroupPermRelatedManager,
)

PERM_TYPE_GENERIC = 'generic'
PERM_TYPE_MODEL = 'model'
PERM_TYPE_OBJECT = 'object'
PERM_TYPE_FIELD = 'field'


DEFAULT_PERM_CODENAMES = {
    'add': _('Add permission'),
    'change': _('Change permission'),
    'delete': _('Delete permission'),
}

PERM_CODENAMES = dict(DEFAULT_PERM_CODENAMES, **perm_settings.PERM_CODENAMES)


class Perm(models.Model):
    name = models.CharField(_('name'), max_length=255)
    codename = models.CharField(_('codename'), max_length=100)
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('content type'),
        blank=True,
        null=True,
    )
    object_id = models.SmallIntegerField(_('object pk'), null=True, blank=True)
    content_object = GenericForeignKey()
    field_name = models.CharField(_('field name'), max_length=100, null=True, blank=True)

    objects = PermManager()

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        ordering = ('codename',)
        unique_together = ('codename', 'content_type', 'object_id', 'field_name')

    def __str__(self):
        return self.name

    @cached_property
    def is_model_perm(self):
        return (
            self.content_type is not None
            and self.field_name is None
            and self.object_id is None
        )

    @cached_property
    def is_object_perm(self):
        return (
            self.content_type is not None
            and self.object_id is not None
        )

    @cached_property
    def is_field_perm(self):
        return self.field_name is not None

    @cached_property
    def is_generic_perm(self):
        return (
            self.content_type is None
            and self.field_name is None
            and self.object_id is None
            and self.codename
        )

    def get_generated_name(self):
        permission_name = str(PERM_CODENAMES.get(self.codename, 'Permission'))

        if self.is_model_perm:
            name = _('for model %s') % (
                self.model.__name__
            )
        elif self.is_object_perm:
            name = _('for %s on model %s') % (
                self.content_object,
                self.model.__name__
            )
        elif self.is_field_perm:
            name = _('for field %s on model %s') % (
                self.model._meta.get_field(self.field_name).verbose_name,
                self.model.__name__
            )
        else:
            name = ''

        return ' '.join((permission_name, name))

    @cached_property
    def model(self):
        return self.content_type.model_class()

    def save(self, *args, **kwargs):
        if self.name in EMPTY_VALUES:
            self.name = self.get_generated_name()

        super().save(*args, **kwargs)


class UserPerm(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userperms')
    perm = models.ForeignKey(Perm, on_delete=models.CASCADE, related_name='userperms')

    # objects = UserPermManager()

    class Meta:
        verbose_name = _('user perm')
        verbose_name_plural = _('user perms')
        ordering = ('user',)
        unique_together = ('user', 'perm')

    def __str__(self):
        return '%s | %s' % (
            self.user,
            self.perm
        )


class GroupPerm(models.Model):

    group = models.ForeignKey(Group, related_name='groupperms')
    perm = models.ForeignKey(Perm, on_delete=models.CASCADE, related_name='groupperms')

    # objects = GroupPermManager()

    class Meta:
        verbose_name = _('group perm')
        verbose_name_plural = _('group perms')
        ordering = ('group',)
        unique_together = ('group', 'perm')

    def __str__(self):
        return '%s | %s' % (
            self.group,
            self.perm
        )


def monkey_patch_user():
    user_model = get_user_model()
    setattr(user_model, 'perms', property(lambda self: UserPermRelatedManager(UserPerm, self)))


def monkey_patch_group():
    setattr(Group, 'perms', property(lambda self: GroupPermRelatedManager(GroupPerm, self)))


monkey_patch_user()
monkey_patch_group()
