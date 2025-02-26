from django.urls import include, path
from .views import index, file_list

app_name = 'mlapp'
urlpatterns = [
    path('files/', file_list, name='file_list'),
    path('prediksi/', include('mlprojek.prediksi.urls', namespace='prediksi')),
    path('klasifikasi/', include('mlprojek.klasifikasi.urls', namespace='klasifikasi')),
    path('', index, name='index'),
]
