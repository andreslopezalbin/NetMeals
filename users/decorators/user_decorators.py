from django.contrib.auth.decorators import user_passes_test


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u is not None and u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, "/no_permission", None)

def anonymous_required(redirect_to="/"):
    def is_anonymous_required(u):
        return u.is_anonymous()

    return user_passes_test(is_anonymous_required, redirect_to, None)


