import datetime
from pathlib import Path
from django.shortcuts import render
from fitur.scraping.views import get_bmkg_data
from mlprojek.prediksi.views import get_hasil_prediksi_data

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorSmartACData
from .helper2 import process_sensor_data

import random
# Create your views here.

is_receiving = True

def index(request):
    return render(request, 'skripsi/index.html')

def remote(request):
    return render(request, 'skripsi/remote.html')

def data(request):
    context = get_bmkg_data(request) 
    # Cek jika terjadi error saat mengambil data
    if 'error' in context:
        return render(request, 'scraping/datascrapingbmkg.html', {'error': context['error']})
    return render(request, 'skripsi/data.html', context)

def prediksi_list(request):
    """Menampilkan halaman dengan data prediksi"""
    result = get_hasil_prediksi_data()

    if "error" in result:
        return render(request, "skripsi/prediksi.html", {"error": result["error"]}, status=result["status"])

    return render(request, "skripsi/prediksi.html", {"files": result["files"]})

def dashboard(request):
    return render(request, 'skripsi/dashboard.html')

@csrf_exempt
def receive_data_ac(request):
    return process_sensor_data(request)

def get_data_ac(request):
    """ Mengambil data dari database dan mengembalikannya dalam format JSON """
    data = SensorSmartACData.objects.order_by('-timestamp').values("timestamp","tempout", "humiout", "tempac", "modeac", "hasilpred")
    return JsonResponse(list(data), safe=False)

import joblib
import json
import pandas as pd
from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from sklearn.preprocessing import MinMaxScaler

def manual_prediction(request):
    model_path = Path(settings.MEDIA_ROOT) / "models/prediksi"
    model_file = model_path / f"svr_model_data.csv.joblib"
    metadata_file = model_path / f"svr_metadata_data.csv.json"
    scaler_path = model_path / f"scaler_data.csv.joblib"

    fitur = []
    target = ""
    predicted_value = None

    # Cek apakah metadata tersedia
    if metadata_file.exists():
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
        fitur = metadata.get("fitur", [])
        target = metadata.get("target", "")

    if request.method == "POST":
        input_data = []

        # Ambil nilai input dari form
        for f in fitur:
            try:
                value = float(request.POST.get(f, 0))
                input_data.append(value)
            except ValueError:
                return JsonResponse({"error": f"Input untuk {f} harus berupa angka."}, status=400)

        if model_file.exists() and scaler_path.exists():
            try:
                # Load model dan scaler
                svr = joblib.load(model_file)
                scaler = joblib.load(scaler_path)

                # Skalakan input dengan scaler yang sama
                input_data_scaled = scaler.transform([input_data])

                # Prediksi nilai
                predicted_value = svr.predict(input_data_scaled)[0]
            except Exception as e:
                return JsonResponse({"error": f"Gagal melakukan prediksi: {str(e)}"}, status=500)
        else:
            return JsonResponse({"error": "Model atau scaler tidak ditemukan. Silakan lakukan pelatihan model terlebih dahulu."}, status=500)

    return render(request, "skripsi/manual_prediction.html", {
        "fitur": fitur,
        "target": target,
        "predicted_value": predicted_value,
    })
