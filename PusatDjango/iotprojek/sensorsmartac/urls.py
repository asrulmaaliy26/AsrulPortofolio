from django.urls import path
from .views import receive_data, index, get_data, upload_dataset

app_name = 'sensorsmartac'
urlpatterns = [
    path("", index, name="index"),
    path("data/", get_data, name="get_data"),
    path("api/receive/", receive_data, name="receive_data"),
    path("upload_dataset/", upload_dataset, name="upload_dataset"),
]
