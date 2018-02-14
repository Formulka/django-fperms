from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models, IntegrityError
from django.utils.functional import cached_property, curry
from django.utils.translation import ugettext as _

from model_utils.models import TimeStampedModel


DEFAULT_PERMISSION_NAMES = {
    'add': _('Add permission '),
    'update': _('Update permission '),
    'delete': _('Delete permission '),
}

PERMISSION_NAMES = DEFAULT_PERMISSION_NAMES.update(settings.PERMS_PERMISSION_NAMES)


class BasePermission:
    ...


class Permission(TimeStampedModel):

    name = models.CharField(_('name'), max_length=255)
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('content type'),
        blank=True,
        null=True,
    )
    codename = models.CharField(_('codename'), max_length=100, null=True, blank=True)
    object_pk = models.SmallIntegerField(_('object pk'), null=True, blank=True)
    field_name = models.CharField(_('field name'), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        ordering = ('codename',)
        unique_together = ('code', 'content_type', 'object_pk', 'field_name')

    def __str__(self):

        return '%s | %s' % (
            self.codename,
            self.name
        )

    @cached_property
    def is_model_permission(self):
        return (
            self.content_type is not None
            and self.field_name is None
            and self.object_pk is None
        )

    @cached_property
    def is_object_permission(self):
        return (
            self.content_type is not None
            and self.object_pk is not None
        )

    @cached_property
    def is_field_permission(self):
        return self.field_name is not None

    @cached_property
    def is_generic_permission(self):
        return (
            self.content_type is None
            and self.field_name is None
            and self.object_pk is None
            and self.codename
        )

    def get_generated_name(self):
        permission_name = PERMISSION_NAMES.get(self.codename)

        if self.is_model_permission:
            name = _('for model %s') % (
                self.model
            )
        elif self.is_object_permission:
            name = _('for object %s on model %s') % (
                self.instance,
                self.model
            )
        elif self.is_field_permission:
            name = _('for field %s on model %s') % (
                self.model._meta.get_field(self.field_name).verbose_name,
                self.model
            )
        else:
            name = ''

        return ' '.join((permission_name, name))

    @cached_property
    def model(self):
        return self.content_type.model

    @cached_property
    def instance(self):
        return self.model.get(pk=self.object_pk) if self.is_object_permission else None

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.name is None:
            self.name = self.get_generated_name()

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
