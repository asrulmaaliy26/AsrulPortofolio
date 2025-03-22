from django.urls import path
from .views import receive_data, index, get_data, get_data_from_db, get_temp_log, view_temp_log, export_csv, export_excel, export_pdf, upload_dataset

app_name = 'sensorkualitasudara'
urlpatterns = [
    path("", index, name="index"),
    path("data/", get_data, name="get_data"),
     path('get_data_db/', get_data_from_db, name='get_data_from_db'),
    path("api/receive/", receive_data, name="receive_data"),
    path("view_temp_log/", view_temp_log, name="view_temp_log"),
    path("get_temp_log/", get_temp_log, name="get_temp_log"),
    path("export/csv/", export_csv, name="export_csv"),
    path("export/excel/", export_excel, name="export_excel"),
    path("export/pdf/", export_pdf, name="export_pdf"),
    path("upload_dataset/", upload_dataset, name="upload_dataset"),
]
