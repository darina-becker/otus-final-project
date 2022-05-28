import django.forms
from django.forms import ModelForm

from app.models import App, Comment, Rating


# TODO create own form for create
class AppCreateForm(ModelForm):
    class Meta:
        model = App
        fields = ['name', 'desc', 'kind', 'age_limit', 'category', 'apkfile']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AppCreateForm, self).__init__(*args, **kwargs)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rate']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RatingForm, self).__init__(*args, **kwargs)
