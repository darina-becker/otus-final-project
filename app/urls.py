from django.urls import path

import app.views as app

app_name = 'apps'

urlpatterns = [
    path('detail/<int:pk>/', app.AppDetailView.as_view(), name='detail'),
    path('create/', app.AppCreateView.as_view(), name='create'),
    path('list/', app.AppListView.as_view(), name='list'),
    path('download/<int:pk>', app.download, name='download'),
]
