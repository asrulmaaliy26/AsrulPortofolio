from django.urls import path
from . import views

app_name = 'compress'
urlpatterns = [
    path('upload_image/', views.upload_image, name='upload_image'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('example/', views.ExampleView.as_view(), name='example'),
    path('', views.index, name='index'),
]

