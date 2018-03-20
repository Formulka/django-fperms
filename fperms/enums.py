from fperms.conf import settings
from django.utils.translation import ugettext_lazy as _


PERM_CODENAME_ADD = 'add'
PERM_CODENAME_CHANGE = 'change'
PERM_CODENAME_DELETE = 'delete'
PERM_CODENAME_WILDCARD = '*'

DEFAULT_PERM_CODENAMES = {
    PERM_CODENAME_ADD: _('add'),
    PERM_CODENAME_CHANGE: _('change'),
    PERM_CODENAME_DELETE: _('delete'),
    PERM_CODENAME_WILDCARD: _('wildcard'),
}

PERM_CODENAMES = dict(DEFAULT_PERM_CODENAMES, **settings.PERM_CODENAMES)

PERM_TYPE_GENERIC = 'generic'
PERM_TYPE_MODEL = 'model'
PERM_TYPE_OBJECT = 'object'
PERM_TYPE_FIELD = 'field'

DEFAULT_PERM_TYPE_CHOICES = (
    (PERM_TYPE_GENERIC, _('generic')),
    (PERM_TYPE_MODEL, _('model')),
    (PERM_TYPE_OBJECT, _('object')),
    (PERM_TYPE_FIELD, _('field')),
)

PERM_TYPE_CHOICES = DEFAULT_PERM_TYPE_CHOICES + settings.PERM_TYPE_CHOICES
