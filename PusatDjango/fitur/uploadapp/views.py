import json
from django.core.paginator import Paginator
from pathlib import Path
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from .utils import get_data_dir, get_uploaded_files, get_unique_file_path, save_uploaded_file, extract_file_columns, ambil_data

# urls
def index(request):
    return render(request, 'uploadapp/index.html')


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        new_file_name = request.POST.get('new_file_name', '').strip() or Path(uploaded_file.name).stem
        file_extension = Path(uploaded_file.name).suffix.lower()
        upload_dir = get_data_dir()
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

# urls
def file_list(request):
    return render(request, 'uploadapp/file_list.html', {"files": get_uploaded_files()})

#urls
def view_file(request):
    file_name = request.GET.get('file_name')
    if not file_name:
        return JsonResponse({"error": "File name is required"}, status=400)
    
    file_path = get_data_dir() / file_name
    if not file_path.exists():
        return JsonResponse({"error": "File not found"}, status=404)
    
    response = ambil_data(request, file_name)
    if response.status_code != 200:
        return response
    
    data = json.loads(response.content).get("data", [])
    per_page = request.GET.get('per_page', 10)
    
    if per_page == 'all':
        page_obj = data
    else:
        paginator = Paginator(data, int(per_page))
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    return render(request, 'uploadapp/file_preview.html', {"file_name": file_name, "page_obj": page_obj, "per_page": per_page})

def delete_file(request):
    if request.method == "POST":
        file_name = request.POST.get("file_name")
        file_path = get_data_dir() / file_name
        
        if file_path.exists():
            file_path.unlink()
            return JsonResponse({"message": f"File {file_name} deleted successfully", "success": True})
        return JsonResponse({"error": "File not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request"}, status=400)
