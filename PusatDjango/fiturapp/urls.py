from django.urls import include, path
from . import views

app_name = 'fiturapp'
urlpatterns = [
    
    path('compress/', include('fitur.compress.urls', namespace='compress')),
    path('convert/', include('fitur.convert.urls', namespace='convert')),
    path('scraping/', include('fitur.scraping.urls', namespace='scraping')),
    path('uploadapp/', include('fitur.uploadapp.urls', namespace='uploadapp')),
    path('example/', views.ExampleView.as_view(), name='example'),
    path('', views.index, name='index'),
]
