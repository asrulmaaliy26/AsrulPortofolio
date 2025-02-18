from pathlib import Path
import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
import pythoncom
from win32com.client import Dispatch
import json

def index(request):
    return render(request, 'uploadapp/index.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file') and request.POST.get('new_file_name'):
        uploaded_file = request.FILES['file']
        new_file_name = request.POST['new_file_name']
        file_extension = Path(uploaded_file.name).suffix.lower()
        renamed_file = f"{new_file_name}{file_extension}"
        save_path = Path(settings.MEDIA_ROOT) / 'uploadapp' / renamed_file

        # Pastikan folder target ada
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Simpan file (replace jika sudah ada)
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        response_data = {"message": "File uploaded successfully", "file_name": renamed_file, "success": True}

        if file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(save_path)
            response_data["columns"] = list(df.columns)

        return JsonResponse(response_data)

    # Dapatkan daftar file yang telah diunggah
    upload_dir = Path(settings.MEDIA_ROOT) / 'uploadapp'
    files = []
    if upload_dir.exists():
        files = [{"name": f.name, "format": f.suffix} for f in upload_dir.iterdir() if f.is_file()]

    return render(request, 'uploadapp/upload.html', {"files": files})

def file_list(request):
    """View untuk menampilkan daftar file yang telah diunggah."""
    upload_dir = Path(settings.MEDIA_ROOT) / 'uploadapp'
    files = []
    
    if upload_dir.exists():
        files = [{"name": f.name, "format": f.suffix} for f in upload_dir.iterdir() if f.is_file()]

    return render(request, 'uploadapp/file_list.html', {"files": files})


def view_excel_file(request):
    """View untuk menampilkan isi file Excel yang dipilih."""
    file_name = request.GET.get('file_name')
    if not file_name:
        return JsonResponse({"error": "File name is required"}, status=400)

    file_path = Path(settings.MEDIA_ROOT) / 'uploadapp' / file_name

    if not file_path.exists():
        return JsonResponse({"error": "File not found"}, status=404)

    try:
        df = pd.read_excel(file_path)
        data = df.to_dict(orient="records")  # Konversi ke JSON
        return render(request, 'uploadapp/file_preview.html', {"file_name": file_name, "data": data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)