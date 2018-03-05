__version__ = '0.1.0'

from django.apps import apps as django_apps
from django_perms.conf import settings

from django_perms.exceptions import ImproperlyConfigured


def get_perm_model():
    """
    Returns the User model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.PERM_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("PERM_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "PERM_MODEL refers to model '%s' that has not been installed" % settings.PERM_MODEL
        )
