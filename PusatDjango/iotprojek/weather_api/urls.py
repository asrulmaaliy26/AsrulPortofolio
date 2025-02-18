from django.urls import path
from . import views

app_name = 'weatherapi'
urlpatterns = [
    path('', views.index, name='index'),
    path('getapi/', views.get_weather_data, name='getapi'),
]

