from fperms.base import BasePerm, Group
from fperms.managers import RelatedPermManager


class Perm(BasePerm):

    related_manager = RelatedPermManager()

    class Meta:
        base_manager_name = 'related_manager'
