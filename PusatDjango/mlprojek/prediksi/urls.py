from django.urls import path
from .views import index, hapus_colom_file, prediksi_svr, prediksi_list

app_name = 'prediksi'
urlpatterns = [
    path('', index, name='index'),
    path('prediksi_list', prediksi_list, name='prediksi_list'),
    path('haspus-colom-file/<str:file_name>/', hapus_colom_file, name='hapus_colom_file'),
    path('prediksi_svr/<str:file_name>/', prediksi_svr, name='prediksi_svr'),
]
