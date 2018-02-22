from __future__ import unicode_literals


class PermError(Exception):
    pass


class ObjectNotPersisted(PermError):
    pass


class PermNotUnique(PermError):
    pass
