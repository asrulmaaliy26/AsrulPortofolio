from django.urls import path
from .views import upload_file, index, file_list, view_file, delete_file

app_name = 'uploadapp'
urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
    path('view_file/', view_file, name='view_file'),
    path('delete_file/', delete_file, name='delete_file'),
]
