from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test

from account.models import Account
from developer.forms import DevAccountCreateForm
from developer.models import DevAccount


@login_required
def index(request):
    req = request.user.is_developer
    if req is not None:
        context = {
            'dev_name': request.user.dev_name
        }
        return render(request, 'dev/index.html', context=context)
    else:
        return render(request, 'dev/index.html')


class DevAccountCreateView(LoginRequiredMixin, CreateView):
    model = DevAccount
    success_url = '/'
    form_class = DevAccountCreateForm

    def get_form_kwargs(self):
        kwargs = super(DevAccountCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        dev_form = form.save(commit=False)
        dev_form.user = self.request.user
        dev_form.save()

        Account.objects.filter(pk=self.request.user.pk).update(is_developer=True)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('devs:dev_main')
