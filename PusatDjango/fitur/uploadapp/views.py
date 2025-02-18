from pathlib import Path
import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
import pythoncom
from win32com.client import Dispatch

def index(request):
    return render(request, 'uploadapp/index.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        save_path = Path(settings.MEDIA_ROOT) / 'uploadapp' / file_name

        # Pastikan folder target ada
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Simpan file (replace jika sudah ada)
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Cek tipe file
        file_extension = save_path.suffix.lower()
        response_data = {"message": "File uploaded successfully", "file_name": file_name}

        if file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(save_path)
            response_data["columns"] = list(df.columns)

        elif file_extension in ['.doc', '.docx']:
            try:
                pythoncom.CoInitialize()
                word = Dispatch("Word.Application")
                doc = word.Documents.Open(str(save_path))
                text = doc.Content.Text
                doc.Close(False)
                word.Quit()
                response_data["content_preview"] = text[:500]  # Preview teks maksimal 500 karakter
            except Exception as e:
                response_data["error"] = str(e)

        return JsonResponse(response_data)

    return render(request, 'uploadapp/upload.html')
