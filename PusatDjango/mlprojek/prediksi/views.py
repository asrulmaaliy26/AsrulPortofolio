import json
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
import pandas as pd
import json

def prediksi_svr(request, file_name):
    response = ambil_data(request, file_name)
    response_data = json.loads(response.content)

    if response.status_code != 200:
        return render(request, "prediksi/prediksi_svr.html", {"file_name": file_name, "error": response_data.get("error"), "columns": []})

    df = pd.DataFrame(response_data.get("data", []))
    predicted_value, mae, mape, r2 = None, None, None, None  # Inisialisasi metrik

    if request.method == "POST":
        fitur = request.POST.getlist("fitur")
        target = request.POST.get("target")

        if fitur and target and target in df.columns:
            # Konversi kolom non-numerik ke angka menggunakan Label Encoding
            for col in fitur + [target]:
                if df[col].dtype == 'object':
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col])

            # Menghapus atau menangani NaN
            df.dropna(inplace=True)

            # Imputasi NaN dengan mean jika masih ada
            imputer = SimpleImputer(strategy="mean")
            df[fitur] = imputer.fit_transform(df[fitur])
            df[target] = imputer.fit_transform(df[[target]])

            X = df[fitur]
            y = df[target]

            if X.shape[1] > 0 and y.shape[0] > 0:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                svr = SVR()
                svr.fit(X_train_scaled, y_train)

                y_pred = svr.predict(X_test_scaled)

                # Hitung metrik evaluasi
                mae = mean_absolute_error(y_test, y_pred)
                mape = mean_absolute_percentage_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)

                if not X_test_scaled.size == 0:
                    predicted_value = y_pred[0]

    return render(request, "prediksi/prediksi_svr.html", {
        "file_name": file_name,
        "columns": df.columns.tolist(),
        "predicted_value": predicted_value,
        "mae": mae,
        "mape": mape,
        "r2": r2,
        "table_data": df.head(5).to_html(classes="table table-bordered table-striped", index=False)  # Hanya 5 baris pertama
})
