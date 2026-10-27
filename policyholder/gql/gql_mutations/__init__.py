# flake8: noqa
from .input_types import *


class LiveTargetMixin:
    """Update, delete and replace act on live rows only.

    The shared mutation mixins look their target up through the model's
    get_queryset (core target_queryset). That no longer hides soft-deleted
    rows - the resolvers decide it, so "show deleted" can list them - so the
    write paths say it here, and a deleted row stays read-only as before.
    Place it before the core mixin in the bases.
    """

    @classmethod
    def _target_queryset(cls, user):
        return super()._target_queryset(user).filter(is_deleted=False)
