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

def prediksi_svr(request, file_name):
    response = ambil_data(request, file_name)
    response_data = json.loads(response.content)

    if response.status_code != 200:
        return render(request, "prediksi/prediksi_svr.html", {"file_name": file_name, "error": response_data.get("error"), "columns": []})

    df = pd.DataFrame(response_data.get("data", []))
    predicted_value, mae, mape, r2 = None, None, None, None  
    fitur, target = [], None

    model_path = Path(settings.MEDIA_ROOT) / "models/prediksi"
    model_path.mkdir(parents=True, exist_ok=True)
    model_file = model_path / f"svr_model_{file_name}.pkl"
    metadata_file = model_path / f"svr_metadata_{file_name}.json"

    if metadata_file.exists():
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
        fitur = metadata["fitur"]
        target = metadata["target"]
        
    if request.method == "POST":
        fitur = request.POST.getlist("fitur")
        target = request.POST.get("target")

        if fitur and target and target in df.columns:
            for col in fitur + [target]:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype('category').cat.codes

            df.dropna(inplace=True)

            imputer = SimpleImputer(strategy="mean")
            df[fitur] = imputer.fit_transform(df[fitur])
            df[target] = imputer.fit_transform(df[[target]])

            X = df[fitur]
            y = df[target]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            metadata = {"fitur": fitur, "target": target}
            with open(metadata_file, "w") as f:
                json.dump(metadata, f)

            if model_file.exists():
                svr = joblib.load(model_file)
            else:
                svr = SVR()
                svr.fit(X_train_scaled, y_train)
                joblib.dump(svr, model_file)

            y_pred = svr.predict(X_test_scaled)

            mae = mean_absolute_error(y_test, y_pred)
            mape = mean_absolute_percentage_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            predicted_value = y_pred[0] if y_pred.size > 0 else None

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