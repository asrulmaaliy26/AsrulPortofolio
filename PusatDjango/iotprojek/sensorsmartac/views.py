from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .models import SensorSuhuACData
from .helper import process_sensor_data

def index(request):
    return render(request, "sensorsmartac/index.html")

@csrf_exempt
def receive_data(request):
    return process_sensor_data(request, allow_extra_fields=False)

def get_data(request):
    """ Mengambil data dari database dan mengembalikannya dalam format JSON """
    data = SensorSuhuACData.objects.order_by('-timestamp').values("timestamp", "ppm", "temp", "humi", "tempout", "humiout", "tempac", "modeac")
    return JsonResponse(list(data), safe=False)

def upload_dataset(request):
    """ Mengexport data dari database ke CSV sesuai nama file yang diinput user """
    if request.method != "POST":
        return HttpResponse("Metode tidak diizinkan.", status=405)

    filename = request.POST.get("filename", "").strip()
    if not filename:
        filename = "dataset.csv"
    elif not filename.lower().endswith(".csv"):
        filename += ".csv"

    # Ambil data dari database
    data = SensorSuhuACData.objects.values("timestamp", "ppm", "temp", "humi", "tempout", "humiout", "tempac", "modeac")
    if not data:
        return HttpResponse("Tidak ada data untuk diekspor.", content_type="text/plain")

    # Konversi ke DataFrame dan simpan ke CSV
    df = pd.DataFrame(list(data))
    df.rename(columns={"timestamp": "Waktu", "ppm": "PPM", "temp": "Temp", "humi": "Humidity", "tempout": "TempOut", "humiout": "HumidityOut", "tempac": "TempAC", "modeac": "ModeAC" }, inplace=True)

    # Simpan ke folder media
    dataset_path = settings.MEDIA_ROOT / 'data'
    dataset_path.mkdir(parents=True, exist_ok=True)
    csv_path = dataset_path / filename
    df.to_csv(csv_path, index=False)

    return redirect(reverse('fiturapp:uploadapp:file_list'))
