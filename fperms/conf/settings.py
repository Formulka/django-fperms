from django.conf import settings

PERM_TYPE_CHOICES = getattr(settings, 'EXTRA_PERM_TYPE_CHOICES', ())

PERM_CODENAMES = getattr(settings, 'PERM_CODENAMES', {})

PERM_MODEL = getattr(settings, 'PERM_MODEL', 'fperms.Perm')
PERM_AUTO_CREATE = getattr(settings, 'PERM_AUTO_CREATE', False)
