from django.urls import path
from .views import index

app_name = 'klasifikasi'
urlpatterns = [
    path('', index, name='index'),
]
