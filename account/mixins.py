from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


class IsDeveloperMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_developer:
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)