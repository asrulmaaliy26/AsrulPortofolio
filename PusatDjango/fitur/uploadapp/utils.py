import json
from pathlib import Path
import pandas as pd
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

def get_data_dir():
    """Mengembalikan path direktori upload."""
    upload_dir = Path(settings.MEDIA_ROOT) / 'data'
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

def get_uploaded_files():
    """Mengembalikan daftar file dalam direktori upload."""
    return [{"name": f.name, "format": f.suffix} for f in get_data_dir().iterdir() if f.is_file()]

def load_dataframe(file_path):
    """Membaca file berdasarkan formatnya dan mengembalikannya sebagai DataFrame."""
    try:
        if file_path.suffix.lower() == ".csv":
            return pd.read_csv(file_path, encoding='latin1')
        elif file_path.suffix.lower() in (".xls", ".xlsx"):
            return pd.read_excel(file_path)
        return None
    except Exception as e:
        raise ValueError(f"Error membaca file: {e}")

def ambil_data(request, file_name):
    file_path = get_data_dir() / file_name
    df = load_dataframe(file_path)
    if df is None:
        return JsonResponse({"error": "Format file tidak didukung."}, status=400)
    return JsonResponse({"file_name": file_name, "data": df.to_dict(orient='records')})

def get_unique_file_path(upload_dir, file_name, file_extension):
    """Menghasilkan nama file unik jika sudah ada yang sama."""
    save_path = upload_dir / f"{file_name}{file_extension}"
    counter = 1
    while save_path.exists():
        save_path = upload_dir / f"{file_name} ({counter}){file_extension}"
        counter += 1
    return save_path\

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