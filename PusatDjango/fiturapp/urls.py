from django.contrib import admin
from django.urls import path
from . import views

app_name = 'fitruapp'
urlpatterns = [
    path('upload_image/', views.upload_image, name='upload_image'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('', views.index, name='index'),
]
