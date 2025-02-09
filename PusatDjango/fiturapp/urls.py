from django.urls import include, path
from . import views

app_name = 'fiturapp'
urlpatterns = [
    
    path('compress/', include('fitur.compress.urls', namespace='compress')),
    path('scraping/', include('fitur.scraping.urls', namespace='scraping')),
    path('example/', views.ExampleView.as_view(), name='example'),
    path('', views.index, name='index'),
]
