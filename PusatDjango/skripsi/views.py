import requests
import pandas as pd
import pvlib
from datetime import datetime
import pytz
from django.shortcuts import render
from fitur.scraping.views import get_bmkg_data

# Create your views here.

def index(request):
    return render(request, 'skripsi/index.html')

def data(request):
    context = get_bmkg_data(request) 
    # Cek jika terjadi error saat mengambil data
    if 'error' in context:
        return render(request, 'scraping/datascrapingbmkg.html', {'error': context['error']})
    return render(request, 'skripsi/data.html', context)
