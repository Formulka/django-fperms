__version__ = '0.4.3'

from django.apps import apps as django_apps
from fperms.conf import settings

from fperms.exceptions import ImproperlyConfigured


def get_perm_model():
    """
    Returns the Perm model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.PERM_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("PERM_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "PERM_MODEL refers to model '{}' that has not been installed".format(settings.PERM_MODEL)
        )
