from django.urls import path
from .views import receive_data, index, get_data,  get_temp_log, view_temp_log, export_csv, export_excel, export_pdf, upload_dataset
from .view_db import receive_to_db, get_data_from_db, upload_dataset_from_db, indexdb

app_name = 'sensorkualitasudara'
urlpatterns = [
    path("", index, name="index"),
    path("indexdb", indexdb, name="indexdb"),
    #pake file
    path("data/", get_data, name="get_data"),
    path('get_data_db/', get_data_from_db, name='get_data_from_db'),
    path("api/receive/", receive_data, name="receive_data"),
    #pake Database
    path("receive_db/", receive_to_db, name="receive_to_db"),
    path("view_temp_log/", view_temp_log, name="view_temp_log"),
    path("get_temp_log/", get_temp_log, name="get_temp_log"),
    path("export/csv/", export_csv, name="export_csv"),
    path("export/excel/", export_excel, name="export_excel"),
    path("export/pdf/", export_pdf, name="export_pdf"),
    path("upload_dataset/", upload_dataset, name="upload_dataset"),
    path("upload_dataset_from_db/", upload_dataset_from_db, name="upload_dataset_from_db"),
]
