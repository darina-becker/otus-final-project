from django.contrib.auth.forms import UserCreationForm

from account.models import Account


class AccountCreateForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email', 'birth_date', 'password1', 'password2')


