from django.urls import path
from .views import HomeView, ImageUploadView, FileUploadView, ExampleView

app_name = 'compress'
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('upload_image/', ImageUploadView.as_view(), name='upload_image'),
    path('upload_file/', FileUploadView.as_view(), name='upload_file'),
    path('example/', ExampleView.as_view(), name='example'),
]

