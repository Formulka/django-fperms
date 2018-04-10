from django.conf import settings as django_settings


DEFAULTS = {
    'PERM_TYPE_CHOICES': (),
    'PERM_CODENAMES': {},
    'PERM_MODEL': 'fperms.Perm',
    'PERM_AUTO_CREATE': False,
}


class Settings:

    def __getattr__(self, attr):
        if attr not in DEFAULTS:
            raise AttributeError('Invalid fperms setting: "{}"'.format(attr))

        default = DEFAULTS[attr]
        return getattr(django_settings, attr, default(self) if callable(default) else default)


settings = Settings()
