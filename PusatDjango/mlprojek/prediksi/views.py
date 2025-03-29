import json
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from fitur.uploadapp.utils import get_uploaded_files, ambil_data, get_data_dir, get_unique_file_path

def index(request):
    """Menampilkan halaman utama dengan daftar file yang diunggah."""
    files = get_uploaded_files()
    return render(request, 'prediksi/index.html', {"files": files})

def hapus_colom_file(request, file_name):
    response = ambil_data(request, file_name)
    response_data = json.loads(response.content)
    if response.status_code != 200:
        return render(request, "prediksi/hasil_jumlah.html", {"file_name": file_name, "total": response_data.get("error"), "table_data": None, "columns": []})
    
    df = pd.DataFrame(response_data.get("data", []))
    total = df.select_dtypes(include=['number']).sum().sum()
    
    if request.method == "POST":
        kolom_hapus = request.POST.getlist("columns")
        df.drop(columns=kolom_hapus, inplace=True, errors='ignore')
        total = df.select_dtypes(include=['number']).sum().sum()
        
        upload_dir = get_data_dir()
        file_extension = ".csv" if file_name.endswith(".csv") else ".xlsx"
        base_name = file_name.rsplit(".", 1)[0]
        unique_file_path = get_unique_file_path(upload_dir, f"edited_{base_name}", file_extension)
        
        df.to_csv(unique_file_path, index=False) if file_extension == ".csv" else df.to_excel(unique_file_path, index=False)
    else:
        unique_file_path = None
    
    return render(request, "prediksi/hasil_jumlah.html", {
        "file_name": file_name,
        "total": total,
        "table_data": df.to_html(classes="table table-bordered table-striped", index=False),
        "columns": df.columns.tolist(),
        "edited_file": unique_file_path.name if unique_file_path else None
    })

import joblib
from pathlib import Path
from django.conf import settings
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
import json
from django.http import JsonResponse

def prediksi_svr(request, file_name):
    response = ambil_data(request, file_name)
    response_data = json.loads(response.content)

    if response.status_code != 200:
        return JsonResponse({"error": response_data.get("error", "Gagal mengambil data")}, status=response.status_code)

    df = pd.DataFrame(response_data.get("data", []))
    if df.empty:
        return JsonResponse({"error": "Dataset kosong atau tidak ditemukan."}, status=400)

    predicted_value, mae, mape, r2 = None, None, None, None  
    fitur, target = [], None
    total_rows = df.shape[0]

    model_path = Path(settings.MEDIA_ROOT) / "models/prediksi"
    model_path.mkdir(parents=True, exist_ok=True)
    model_file = model_path / f"svr_model_{file_name}.joblib"
    metadata_file = model_path / f"svr_metadata_{file_name}.json"
    scaler_path = model_path / f"scaler_{file_name}.joblib"
    
    original_file_name = file_name

    # Load metadata jika ada
    if metadata_file.exists():
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
        fitur = metadata.get("fitur", [])
        target = metadata.get("target")
        mae, mape, r2 = metadata.get("mae"), metadata.get("mape"), metadata.get("r2")
        predicted_value = metadata.get("predicted_value")
        total_rows = metadata.get("total_rows", total_rows)
        original_file_name = metadata.get("original_file_name", file_name)

    if request.method == "POST":
        fitur = request.POST.getlist("fitur")
        target = request.POST.get("target")

        if not fitur:
            return JsonResponse({"error": "Fitur tidak boleh kosong."}, status=400)

        if not target or target not in df.columns:
            return JsonResponse({"error": "Target tidak valid atau tidak ada dalam dataset."}, status=400)

        # Konversi kategori ke numerik
        for col in fitur + [target]:
            if df[col].dtype == 'object':
                df[col] = df[col].astype('category').cat.codes

        df.dropna(inplace=True)

        # Imputasi data yang hilang
        imputer = SimpleImputer(strategy="mean")
        df[fitur] = imputer.fit_transform(df[fitur])
        df[target] = imputer.fit_transform(df[[target]])

        X = df[fitur]
        y = df[target]

        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        if model_file.exists():
            try:
                svr = joblib.load(model_file)
                scaler = joblib.load(scaler_path)
            except Exception as e:
                return JsonResponse({"error": f"Model rusak atau tidak bisa dimuat: {str(e)}"}, status=500)
        else:
            svr = SVR(kernel="linear")
            svr.fit(X_train_scaled, y_train)
            joblib.dump(svr, model_file)
            joblib.dump(scaler, scaler_path)

        y_pred = svr.predict(X_test_scaled)

        mae = mean_absolute_error(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        predicted_value = y_pred[0] if y_pred.size > 0 else None

        metadata = {
            "original_file_name": original_file_name,
            "fitur": fitur,
            "target": target,
            "mae": mae,
            "mape": mape,
            "r2": r2,
            "predicted_value": predicted_value,
            "total_rows": total_rows
        }
        with open(metadata_file, "w") as f:
            json.dump(metadata, f)

    return render(request, "prediksi/prediksi_svr.html", {
        "file_name": file_name,
        "columns": df.columns.tolist(),
        "fitur": fitur,
        "target": target,
        "predicted_value": predicted_value,
        "mae": mae,
        "mape": mape,
        "r2": r2,
        "table_data": df.head(5).to_html(classes="table table-bordered table-striped", index=False)
    })
    # return JsonResponse({
    #     "file_name": file_name,
    #     "columns": df.columns.tolist(),
    #     "fitur": fitur,
    #     "target": target,
    #     "predicted_value": predicted_value,
    #     "mae": mae,
    #     "mape": mape,
    #     "r2": r2,
    #     "table_data": df.head(5).to_dict(orient="records")
    # })

def get_hasil_prediksi_data():
    """Mengambil daftar file JSON di dalam folder models/prediksi dan mengembalikan datanya"""
    model_path = Path(settings.MEDIA_ROOT) / "models/prediksi"

    # Cek apakah folder ada
    if not model_path.exists():
        return {"error": "Folder tidak ditemukan", "status": 404}

    files = list(model_path.glob("*.json"))  # Cari semua file JSON
    json_data = []

    for file in files:
        try:
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)  # Membaca isi file JSON
                json_data.append({
                    "file_name": file.name,
                    "content": data
                })

        except Exception as e:
            return {"error": f"Gagal membaca {file.name}: {str(e)}", "status": 500}

    return {"files": json_data, "status": 200}

def prediksi_list(request):
    """Menampilkan halaman dengan data prediksi"""
    result = get_hasil_prediksi_data()

    if "error" in result:
        return render(request, "prediksi/prediksi.html", {"error": result["error"]}, status=result["status"])

    return render(request, "prediksi/prediksi.html", {"files": result["files"]})
    
    