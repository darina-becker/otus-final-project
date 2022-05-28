from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView

from account.forms import AccountCreateForm
from account.models import Account


class AccountCreateView(CreateView):
    model = Account
    success_url = '/'
    form_class = AccountCreateForm



