import joblib
import json
import numpy as np
from django.http import JsonResponse
from pathlib import Path
from django.conf import settings
from datetime import datetime

import pandas as pd
from .models import SensorSmartACData
from sklearn.preprocessing import MinMaxScaler

# Path ke model
MODEL_DIR = Path(settings.MEDIA_ROOT) / "models/prediksi"
MODEL_FILE = MODEL_DIR / f"svr_model_data.csv.joblib"
METADATA_FILE = MODEL_DIR / f"svr_metadata_data.csv.json"
SCALER_FILE = MODEL_DIR / f"scaler_data.csv.joblib"  # Menambahkan scaler

# Variabel global untuk mengontrol penerimaan data
is_receiving = True

def process_sensor_data(request):
    """ Memproses data sensor dan menyimpannya ke database """
    global is_receiving
    if not is_receiving:
        return JsonResponse({"message": "Penerimaan data dihentikan"}, status=200)

    if request.method != "POST":
        return JsonResponse({"error": "Metode tidak diperbolehkan"}, status=405)

    try:
        # Pastikan request dalam format JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Format data harus JSON"}, status=400)

        # Ambil data dari request
        tempout = data.get("tempout")
        humiout = data.get("humiout")
        tempac = data.get("tempac")
        modeac = data.get("modeac")

        # Validasi data input
        if None in [tempout, humiout, tempac, modeac]:
            return JsonResponse({"error": "Data tidak lengkap"}, status=400)

        try:
            tempout = float(tempout)
            humiout = float(humiout)
            tempac = float(tempac)
            modeac = int(modeac)
        except ValueError:
            return JsonResponse({"error": "Data tidak valid, pastikan angka"}, status=400)

        # Ambil waktu saat data diterima
        timestamp = datetime.now()
        hour_only = int(timestamp.strftime("%H"))  # Ambil hanya jam

        # Periksa apakah model, metadata, dan scaler tersedia
        if not MODEL_FILE.exists() or not METADATA_FILE.exists() or not SCALER_FILE.exists():
            return JsonResponse({"error": "Model, metadata, atau scaler belum tersedia"}, status=500)

        # Muat metadata
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)

        fitur = metadata.get("fitur", [])
        if not fitur:
            return JsonResponse({"error": "Metadata model tidak valid"}, status=500)

        # Susun input data berdasarkan metadata
        input_data_dict = {}
        for fitur_name in fitur:
            if fitur_name.lower() == "waktu":
                input_data_dict[fitur_name] = [hour_only]
            elif fitur_name.lower() == "tempout":
                input_data_dict[fitur_name] = [tempout]
            elif fitur_name.lower() == "humidityout":
                input_data_dict[fitur_name] = [humiout]
            elif fitur_name.lower() == "tempac":
                input_data_dict[fitur_name] = [tempac]
            elif fitur_name.lower() == "modeac":
                input_data_dict[fitur_name] = [modeac]

        # Pastikan jumlah fitur sesuai
        if len(input_data_dict) != len(fitur):
            return JsonResponse({"error": "Data input tidak sesuai dengan model"}, status=400)

        # Buat DataFrame dengan nama kolom yang sesuai
        input_data_df = pd.DataFrame(input_data_dict)

        # Muat scaler dan lakukan transformasi pada data inpclsut
        try:
            scaler = joblib.load(SCALER_FILE)
            input_data_scaled = scaler.transform(input_data_df)  # Pastikan input memiliki kolom yang sesuai
        except Exception as e:
            return JsonResponse({"error": f"Kesalahan memuat scaler atau melakukan transformasi: {str(e)}"}, status=500)

        # Muat model SVR dan lakukan prediksi
        try:
            svr_model = joblib.load(MODEL_FILE)
            hasil_prediksi = svr_model.predict(input_data_scaled)[0]
        except Exception as e:
            return JsonResponse({"error": f"Kesalahan dalam prediksi: {str(e)}"}, status=500)

        # Simpan ke database
        SensorSmartACData.objects.create(
            tempout=tempout,
            humiout=humiout,
            tempac=tempac,
            modeac=modeac,
            hasilpred=hasil_prediksi,
        )

        return JsonResponse({
            "message": "Data berhasil disimpan",
            "hasil_prediksi": hasil_prediksi,
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Kesalahan server: {str(e)}"}, status=500)
