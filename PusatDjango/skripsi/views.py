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

from django.shortcuts import render
from django.http import JsonResponse
import joblib
import json
import numpy as np
from pathlib import Path
from django.conf import settings
from sklearn.preprocessing import StandardScaler

# Path ke model
MODEL_DIR = Path(settings.MEDIA_ROOT) / "models/prediksi"
MODEL_FILE = MODEL_DIR / "svr_model_smartac.csv.pkl"
METADATA_FILE = MODEL_DIR / "svr_metadata_smartac.csv.json"

def manual_prediction(request):
    hasil_prediksi = None
    error_message = None

    if request.method == "POST":
        try:
            # Periksa apakah model dan metadata tersedia
            if not MODEL_FILE.exists() or not METADATA_FILE.exists():
                error_message = "Model atau metadata tidak tersedia."
            else:
                # Muat metadata
                with open(METADATA_FILE, "r") as f:
                    metadata = json.load(f)

                fitur = metadata.get("fitur", [])
                target = metadata.get("target", "")

                if not fitur or not target:
                    error_message = "Metadata model tidak valid."
                else:
                    # Ambil input data berdasarkan fitur dalam metadata
                    input_data = []
                    for fitur_name in fitur:
                        value = request.POST.get(fitur_name.lower(), None)
                        if value is not None:
                            try:
                                input_data.append(float(value))  # Konversi ke float
                            except ValueError:
                                error_message = f"Input untuk {fitur_name} tidak valid."
                                break
                        else:
                            error_message = f"Fitur {fitur_name} tidak ditemukan dalam input."
                            break

                    # Jika tidak ada error dalam input, lanjutkan prediksi
                    if not error_message and len(input_data) == len(fitur):
                        # Standarisasi input data
                        scaler = StandardScaler()
                        input_data = np.array(input_data).reshape(1, -1)
                        input_scaled = scaler.fit_transform(input_data)

                        # Muat model SVR dan lakukan prediksi
                        svr_model = joblib.load(MODEL_FILE)
                        hasil_prediksi = svr_model.predict(input_scaled)[0]
                    else:
                        error_message = "Data input tidak sesuai dengan model."

        except ValueError:
            error_message = "Input tidak valid, pastikan angka sudah benar."

    return render(request, "skripsi/manual_prediction.html", {
        "hasil_prediksi": hasil_prediksi,
        "error_message": error_message,
    })
