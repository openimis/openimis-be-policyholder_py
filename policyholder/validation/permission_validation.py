from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied


class PermissionValidation:

    @classmethod
    def validate_perms(cls, user, perms):
        if not user.has_perms(perms):
            raise PermissionDenied(_("unauthorized"))

    @classmethod
    def validate_policy_holder_user_link(cls, user, policy_holder_id=None, linked_user_id=None):
        """Who may attach which user to which policy holder.

        Attaching a user to a policy holder is not a plain record: the membership
        widens what that user reads (PolicyHolder.get_queryset lets members see
        their policy holders and everything scoped under them, contracts
        included) and lets the policy holder portal rights apply to it
        (has_hybrid_phu_perms). So:

        - the policy holder must be one the caller may already read, otherwise
          the right to create a link would reach every policy holder;
        - a caller may not attach themselves: that would let anyone holding the
          link right grant themselves any policy holder. Linking oneself is left
          to a superuser, whose reads are not narrowed anyway.
        """
        from policyholder.models import PolicyHolder

        if policy_holder_id is not None and not PolicyHolder.get_queryset(
            PolicyHolder.objects.filter(id=policy_holder_id, is_deleted=False), user
        ).exists():
            raise PermissionDenied(_("unauthorized"))
        if (
            linked_user_id is not None
            and str(linked_user_id) == str(user.id)
            and not user.is_superuser
        ):
            raise PermissionDenied(_("unauthorized"))
