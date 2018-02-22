from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel

from django_perms.managers import UserPermissionManager, GroupPermissionManager


class BasePerm(PolymorphicModel):

    name = models.CharField(_('name'), max_length=255)
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('content type'),
    )
    codename = models.CharField(_('codename'), max_length=100)

    class Meta:
        abstract = True


class Perm(BasePerm):

    class Meta:
        unique_together = ('content_type', 'codename')
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')

    def __str__(self):
        return "%s | %s | %s" % (
            self.content_type.app_label,
            self.content_type,
            self.name
        )


class GlobalPerm(BasePerm):

    class Meta:
        unique_together = ('content_type', 'codename')
        verbose_name = _('Global Permission')
        verbose_name_plural = _('Global Permissions')

    def save(self, *args, **kwargs):
        content_type_kwargs = {
            'app_label': self._meta.app_label,
            'model': 'globalpermission'
        }
        ct, created = ContentType.objects.get_or_create(**content_type_kwargs)

        self.content_type = ct
        super().save(*args, **kwargs)


class ObjectPerm(BasePerm):

    object_pk = models.IntegerField()
    content_object = GenericForeignKey(fk_field='object_pk')

    class Meta:
        unique_together = ('content_type', 'codename', 'object_pk')
        verbose_name = _('Object Permission')
        verbose_name_plural = _('Object Permissions')

    def __str__(self):
        return "%s | %s | %s | %s" % (
            self.content_type.app_label,
            self.content_type,
            self.name,
            self.content_object
        )


class FieldPerm(BasePerm):

    field_name = models.CharField(_('field name'), max_length=100)

    class Meta:
        unique_together = ('content_type', 'codename', 'field_name')
        verbose_name = _('Field Permission')
        verbose_name_plural = _('Field Permissions')

    def __str__(self):
        return "%s | %s | %s | %s" % (
            self.content_type.app_label,
            self.content_type,
            self.name,
            self.field_name
        )


class UserPermission(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    permission = models.ForeignKey(Perm, on_delete=models.CASCADE)

    objects = UserPermissionManager()


class GroupPermission(models.Model):

    group = models.ForeignKey(Group)
    permission = models.ForeignKey(Perm, on_delete=models.CASCADE)

    objects = GroupPermissionManager()


setattr(Group, 'add_perm', lambda self, perm, obj: GroupPermission.objects.assign_perm(perm, self, obj))
setattr(Group, 'del_perm', lambda self, perm, obj: GroupPermission.objects.remove_perm(perm, self, obj))
