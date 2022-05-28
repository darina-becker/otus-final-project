from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def dev_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, join_url=None):
    """
    Decorator for views that checks that the user is developer, redirecting
    to the join page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_developer,
        login_url=join_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
