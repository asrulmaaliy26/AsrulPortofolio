from django.urls import path

from .import views

app_name = 'skripsi'

urlpatterns = [
    path('', views.index, name='index'),
]

