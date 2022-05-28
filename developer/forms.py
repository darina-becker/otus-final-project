from django.forms import ModelForm

from developer.models import DevAccount


class DevAccountCreateForm(ModelForm):
    class Meta:
        model = DevAccount
        fields = ['dev_username', 'email', 'website', 'phone']

    def __init__(self, *args, **kwargs):
        """Save the request with the form so it can be accessed in clean_*()"""
        self.request = kwargs.pop('request', None)
        super(DevAccountCreateForm, self).__init__(*args, **kwargs)
