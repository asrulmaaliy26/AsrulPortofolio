from django.urls import path
from .views import index, proses_file

app_name = 'prediksi'
urlpatterns = [
    path('', index, name='index'),
    path('proses-file/<str:file_name>/', proses_file, name='proses_file'),
]
