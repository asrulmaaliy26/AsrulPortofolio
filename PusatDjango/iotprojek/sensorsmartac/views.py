import datetime
from pathlib import Path
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random

# Create your views here.

DATA_LOG_PATH = Path("iotprojek/sensorsmartac/data/data.log")
ML_PROJECT_PATH = Path("mlprojek/data/")
is_receiving = True

def index(request):
    return render(request, "sensorsmartac/index.html")

@csrf_exempt
def receive_data(request):
    global is_receiving
    print(f"[DEBUG] Request method: {request.method}")  # Cek metode request

    if not is_receiving:
        return JsonResponse({"message": "Penerimaan data dihentikan"}, status=200)

    if request.method == "POST":
        try:
            nilai_random = random.randint(10, 99)
            
            print(f"[DEBUG] {nilai_random} Raw body: {request.body}")  # Cek isi request
            print(f"[DEBUG] {nilai_random} POST data: {request.POST}")  # Cek data yang diterima

            ppm, temp, humi = request.POST.get("ppm"), request.POST.get("temp"), request.POST.get("humi")
            if not all([ppm, temp, humi]):
                return JsonResponse({"error": "Data tidak lengkap"}, status=400)

            log_entry = f"{datetime.datetime.now().strftime('%H:%M:%S')} | PPM: {ppm} | Temp: {temp} | Hum: {humi}\n"
            DATA_LOG_PATH.write_text(DATA_LOG_PATH.read_text() + log_entry, encoding='utf-8')

            
            return JsonResponse({"message": "Data berhasil diterima", "nilai_random": nilai_random}, status=200)

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return JsonResponse({"error": "Server error"}, status=500)

    return JsonResponse({"error": "Hanya menerima POST"}, status=405)

def read_file_content(file_path):
    return file_path.read_text(encoding='utf-8') if file_path.exists() else "Belum ada data."

def get_data(request):
    return HttpResponse(read_file_content(DATA_LOG_PATH), content_type="text/plain")
