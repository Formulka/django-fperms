from django.conf import settings

PERM_CODENAMES = getattr(settings, 'PERM_CODENAMES', {})
