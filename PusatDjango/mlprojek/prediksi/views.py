import json
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from fitur.uploadapp.views import get_uploaded_files

def index(request):
    """Menampilkan halaman utama dengan daftar file yang diunggah."""
    files = get_uploaded_files()
    return render(request, 'prediksi/index.html', {"files": files})

def load_dataframe(file_path):
    """Membaca file berdasarkan formatnya dan mengembalikannya sebagai DataFrame."""
    try:
        if file_path.suffix.lower() == ".csv":
            return pd.read_csv(file_path, encoding='latin1')
        elif file_path.suffix.lower() in (".xls", ".xlsx"):
            return pd.read_excel(file_path)
        else:
            return None
    except Exception as e:
        raise ValueError(f"Error membaca file: {e}")

def ambil_data(request, file_name):
    """Mengambil data dari file yang dipilih dan mengembalikannya dalam format JSON."""
    file_path = Path(settings.MEDIA_ROOT) / 'data' / file_name
    
    df = load_dataframe(file_path)
    if df is None:
        return JsonResponse({"error": "Format file tidak didukung."}, status=400)
    
    return JsonResponse({"file_name": file_name, "data": df.to_dict(orient='records')})

def proses_file(request, file_name):
    """Membaca file yang dipilih, menjumlahkan angka dalam file, dan memungkinkan penghapusan kolom."""
    response = ambil_data(request, file_name)
    response_data = json.loads(response.content)
    
    if response.status_code != 200:
        return render(request, "prediksi/hasil_jumlah.html", {
            "file_name": file_name,
            "total": response_data.get("error"),
            "table_data": None,
            "columns": [],
        })
    
    df = pd.DataFrame(response_data.get("data", []))
    total = df.select_dtypes(include=['number']).sum().sum()
    
    if request.method == "POST":
        kolom_hapus = request.POST.getlist("columns")
        df.drop(columns=kolom_hapus, inplace=True, errors='ignore')
        total = df.select_dtypes(include=['number']).sum().sum()
        
        edited_file_path = Path(settings.MEDIA_ROOT) / f"edited_{file_name}"
        if file_name.endswith(".csv"):
            df.to_csv(edited_file_path, index=False)
        else:
            df.to_excel(edited_file_path, index=False)
    else:
        edited_file_path = None
    
    return render(request, "prediksi/hasil_jumlah.html", {
        "file_name": file_name,
        "total": total,
        "table_data": df.to_html(classes="table table-bordered table-striped", index=False),
        "columns": df.columns.tolist(),
        "edited_file": edited_file_path.name if edited_file_path else None
    })
