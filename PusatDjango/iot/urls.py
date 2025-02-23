from django.urls import include, path
from . import views

app_name = 'iot'
urlpatterns = [
    
    path('weatherapi/', include('iotprojek.weather_api.urls', namespace='weatherapi')),
    path('weatherdashboard/', include('iotprojek.weather_dashboard.urls', namespace='weatherdashboard')),
    path('sensorkualitasudara/', include('iotprojek.sensorkualitasudara.urls', namespace='sensorkualitasudara')),
    path('example/', views.ExampleView.as_view(), name='example'),
    path('', views.index, name='index'),
]
