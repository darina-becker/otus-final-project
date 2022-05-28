from django.contrib.auth.forms import UserCreationForm

from account.models import Account


class AccountCreateForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'username', 'email', 'birth_date', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'email':
                field.widget.attrs['style'] = 'margin-left: 3em;'
            else:
                field.widget.attrs['style'] = 'margin-left: 1em;'
