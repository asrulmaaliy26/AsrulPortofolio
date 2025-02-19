from django.core.paginator import Paginator
from pathlib import Path
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

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


def view_file(request):
    """View untuk menampilkan isi file (Excel & CSV)."""
    file_name = request.GET.get('file_name')
    if not file_name:
        return JsonResponse({"error": "File name is required"}, status=400)

    file_path = Path(settings.MEDIA_ROOT) / 'uploadapp' / file_name

    if not file_path.exists():
        return JsonResponse({"error": "File not found"}, status=404)

    try:
        file_extension = file_path.suffix.lower()
        df = pd.read_excel(file_path) if file_extension in ['.xls', '.xlsx'] else pd.read_csv(file_path)
        data = df.to_dict(orient="records")  # Konversi ke JSON

        # Ambil parameter 'per_page' dari GET request, jika tidak ada default ke 10
        per_page = request.GET.get('per_page', 10)
        try:
            if per_page == 'all':
                page_obj = data  # Menampilkan semua data tanpa paginasi
            else:
                per_page = int(per_page)
                # Paginasi
                paginator = Paginator(data, per_page)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
        except ValueError:
            per_page = 10  # Default jika per_page tidak valid
            paginator = Paginator(data, per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        return render(request, 'uploadapp/file_preview.html', {
            "file_name": file_name,
            "page_obj": page_obj,
            "per_page": per_page
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def delete_file(request):
    """View untuk menghapus file yang dipilih."""
    if request.method == "POST":
        file_name = request.POST.get("file_name")
        file_path = Path(settings.MEDIA_ROOT) / 'uploadapp' / file_name

        if file_path.exists():
            file_path.unlink()  # Hapus file
            return JsonResponse({"message": f"File {file_name} deleted successfully", "success": True})
        else:
            return JsonResponse({"error": "File not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)
