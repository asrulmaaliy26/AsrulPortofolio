from django.urls import path
from .views import index, hapus_colom_file, prediksi_svr

app_name = 'prediksi'
urlpatterns = [
    path('', index, name='index'),
    path('haspus-colom-file/<str:file_name>/', hapus_colom_file, name='hapus_colom_file'),
    path('predikis_svr/<str:file_name>/', prediksi_svr, name='prediksi_svr'),
]
