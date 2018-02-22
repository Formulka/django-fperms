from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel

from django_perms.exceptions import PermNotUnique
from django_perms.managers import UserPermissionManager, GroupPermissionManager


class Perm(PolymorphicModel):

    name = models.CharField(_('name'), max_length=255)
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('content type'),
    )
    codename = models.CharField(_('codename'), max_length=100)

    _perm_unique_together = ('content_type', 'codename')

    class Meta:
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')

    def __str__(self):
        return "%s | %s | %s" % (
            self.content_type.app_label,
            self.content_type,
            self.name
        )

    def _perm_check_unique_together(self):
        perm_unique_together_kwargs = {}
        for field in self._perm_unique_together:
            perm_unique_together_kwargs.update({field: getattr(self, field)})
        try:
            self._meta.model.objects.get(**perm_unique_together_kwargs)
        except self.DoesNotExist:
            # object is unique
            pass
        else:
            raise PermNotUnique(_('Permission already exists'))

    def save(self, *args, **kwargs):
        if not self.pk:
            self._perm_check_unique_together()
        return super().save(*args, **kwargs)


class GlobalPerm(Perm):

    class Meta:
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


class ObjectPerm(Perm):

    object_pk = models.IntegerField()
    content_object = GenericForeignKey(fk_field='object_pk')

    _perm_unique_together = ('content_type', 'codename', 'object_pk')

    class Meta:
        verbose_name = _('Object Permission')
        verbose_name_plural = _('Object Permissions')

    def __str__(self):
        return "%s | %s | %s | %s" % (
            self.content_type.app_label,
            self.content_type,
            self.name,
            self.content_object
        )


class FieldPerm(Perm):

    field_name = models.CharField(_('field name'), max_length=100)

    _perm_unique_together = ('content_type', 'codename', 'field_name')

    class Meta:
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


def monkey_patch_user():
    user_model = get_user_model()
    setattr(user_model, 'add_perm',
            lambda self, perm, model=None, obj=None, field_name=None:
            UserPermission.objects.assign_perm(perm, self, model, obj, field_name))
    setattr(user_model, 'del_perm',
            lambda self, perm, model=None, obj=None, field_name=None:
            UserPermission.objects.remove_perm(perm, self, model, obj, field_name))


def monkey_patch_group():
    setattr(Group, 'add_perm',
            lambda self, perm, model=None, obj=None, field_name=None:
            GroupPermission.objects.assign_perm(perm, self, model, obj, field_name))
    setattr(Group, 'del_perm',
            lambda self, perm, model=None, obj=None, field_name=None:
            GroupPermission.objects.assign_perm(perm, self, model, obj, field_name))


monkey_patch_user()
monkey_patch_group()
