import django.contrib.auth.views as views
from django.urls import path

import developer.views as developer
from app.views import AuthorAppListView

app_name = 'devs'

urlpatterns = [
    path('', developer.index, name='dev_main'),
    path('join/', developer.DevAccountCreateView.as_view(), name='join'),
    path('myapps/', AuthorAppListView.as_view(), name='myapps'),
]
