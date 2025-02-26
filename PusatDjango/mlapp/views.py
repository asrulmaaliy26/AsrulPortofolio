from django.shortcuts import render
from fitur.uploadapp.views import get_uploaded_files

# Create your views here.
def index(request):
    return render(request, 'mlapp/index.html')

def file_list(request):
    """View untuk menampilkan daftar file yang telah diunggah."""
    files = get_uploaded_files()
    return render(request, 'mlapp/file_list.html', {"files": files})