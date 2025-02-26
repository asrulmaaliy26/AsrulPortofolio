from django.core.paginator import Paginator
from pathlib import Path
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse

# urls
def index(request):
    return render(request, 'uploadapp/index.html')

def get_upload_dir():
    """Mengembalikan path direktori upload."""
    upload_dir = Path(settings.MEDIA_ROOT) / 'data'
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

def get_unique_file_path(upload_dir, file_name, file_extension):
    """Menghasilkan nama file unik jika sudah ada yang sama."""
    save_path = upload_dir / f"{file_name}{file_extension}"
    counter = 1
    while save_path.exists():
        save_path = upload_dir / f"{file_name} ({counter}){file_extension}"
        counter += 1
    return save_path

def save_uploaded_file(uploaded_file, save_path):
    """Menyimpan file yang diunggah ke direktori."""
    with open(save_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

def extract_file_columns(file_path):
    """Mengembalikan daftar kolom dari file Excel atau CSV."""
    file_extension = file_path.suffix.lower()
    try:
        if file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
        elif file_extension == '.csv':
            df = pd.read_csv(file_path)
        else:
            return []
        return list(df.columns)
    except Exception:
        return []

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        new_file_name = request.POST.get('new_file_name', '').strip() or Path(uploaded_file.name).stem
        file_extension = Path(uploaded_file.name).suffix.lower()
        upload_dir = get_upload_dir()
        save_path = get_unique_file_path(upload_dir, new_file_name, file_extension)
        
        save_uploaded_file(uploaded_file, save_path)
        columns = extract_file_columns(save_path)
        
        return JsonResponse({
            "message": "File uploaded successfully",
            "file_name": save_path.name,
            "success": True,
            "columns": columns
        })
    
    return render(request, 'uploadapp/upload.html', {"files": get_uploaded_files()})

def get_uploaded_files():
    """Mengembalikan daftar file dalam direktori upload."""
    upload_dir = get_upload_dir()
    return [{"name": f.name, "format": f.suffix} for f in upload_dir.iterdir() if f.is_file()]

# urls
def file_list(request):
    return render(request, 'uploadapp/file_list.html', {"files": get_uploaded_files()})

# urls
def view_file(request):
    file_name = request.GET.get('file_name')
    if not file_name:
        return JsonResponse({"error": "File name is required"}, status=400)
    
    file_path = get_upload_dir() / file_name
    if not file_path.exists():
        return JsonResponse({"error": "File not found"}, status=404)
    
    try:
        df = pd.read_excel(file_path) if file_path.suffix in ['.xls', '.xlsx'] else pd.read_csv(file_path)
        data = df.to_dict(orient="records")
        per_page = request.GET.get('per_page', 10)
        
        if per_page == 'all':
            page_obj = data
        else:
            paginator = Paginator(data, int(per_page))
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        
        return render(request, 'uploadapp/file_preview.html', {"file_name": file_name, "page_obj": page_obj, "per_page": per_page})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def delete_file(request):
    if request.method == "POST":
        file_name = request.POST.get("file_name")
        file_path = get_upload_dir() / file_name
        
        if file_path.exists():
            file_path.unlink()
            return JsonResponse({"message": f"File {file_name} deleted successfully", "success": True})
        return JsonResponse({"error": "File not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request"}, status=400)
