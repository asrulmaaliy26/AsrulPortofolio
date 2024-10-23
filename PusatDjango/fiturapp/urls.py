from django.contrib import admin
from django.urls import path
from . import views

app_name = 'fitruapp'
urlpatterns = [
    path('upload_image/', views.upload_image, name='upload_image'),
    path('', views.index, name='index'),
]
