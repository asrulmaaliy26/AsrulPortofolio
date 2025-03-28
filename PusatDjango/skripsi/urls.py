from django.urls import path

from .import views
from .import helper2

app_name = 'skripsi'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('get_data_ac', views.get_data_ac, name='get_data_ac'),
    path('api/receive_data_ac/', views.receive_data_ac, name='receive_data_ac'),
    path('data', views.data, name='data'),
    path('prediksi_list', views.prediksi_list, name='prediksi_list'),
    path("manual_prediksi/", views.manual_prediction, name="manual_prediction"),
]