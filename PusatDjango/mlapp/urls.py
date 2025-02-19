from django.urls import include, path
from . import views

app_name = 'mlapp'
urlpatterns = [
    path('prediksi/', include('mlprojek.prediksi.urls', namespace='prediksi')),
    path('klasifikasi/', include('mlprojek.klasifikasi.urls', namespace='klasifikasi')),
    path('', views.index, name='index'),
]
