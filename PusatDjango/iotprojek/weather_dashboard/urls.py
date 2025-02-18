from django.urls import path
from . import views

app_name = 'weatherdashboard'
urlpatterns = [
    path('', views.weather_dashboard, name='index'),
    path('data/', views.get_weather_json, name='weather_json'),
]

