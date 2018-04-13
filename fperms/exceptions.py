class PermError(Exception):
    pass


class ObjectNotPersisted(PermError):
    pass


class IncorrectObject(PermError):
    pass


class IncorrectContentType(PermError):
    pass


class ImproperlyConfigured(PermError):
    pass
