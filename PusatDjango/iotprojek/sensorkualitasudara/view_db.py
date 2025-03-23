from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import datetime
import pandas as pd
from .models import SensorData

is_receiving = True  # Variabel global untuk mengontrol penerimaan data

def indexdb(request):
    return render(request, "sensorkualitasudara/indexdb.html")

@csrf_exempt
def receive_to_db(request):
    """ Menerima data dari sensor dan menyimpannya ke database """
    global is_receiving
    if not is_receiving:
        return JsonResponse({"message": "Penerimaan data dihentikan"}, status=200)

    if request.method == "POST":
        try:
            ppm, temp, humi = request.POST.get("ppm"), request.POST.get("temp"), request.POST.get("humi")
            if not all([ppm, temp, humi]):
                return JsonResponse({"error": "Data tidak lengkap"}, status=400)

            # Simpan ke database
            SensorData.objects.create(ppm=ppm, temp=temp, humi=humi)

            return JsonResponse({"message": "Data berhasil diterima"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Hanya menerima POST"}, status=405)

def get_data_from_db(request):
    """ Mengambil data dari database dan mengembalikannya dalam format JSON """
    data = SensorData.objects.order_by('-timestamp').values("timestamp", "ppm", "temp", "humi")
    return JsonResponse(list(data), safe=False)

def upload_dataset_from_db(request):
    """ Mengexport data dari database ke CSV sesuai nama file yang diinput user """
    if request.method != "POST":
        return HttpResponse("Metode tidak diizinkan.", status=405)

    filename = request.POST.get("filename", "").strip()
    if not filename:
        filename = "dataset.csv"
    elif not filename.lower().endswith(".csv"):
        filename += ".csv"

    # Ambil data dari database
    data = SensorData.objects.values("timestamp", "ppm", "temp", "humi")
    if not data:
        return HttpResponse("Tidak ada data untuk diekspor.", content_type="text/plain")

    # Konversi ke DataFrame dan simpan ke CSV
    df = pd.DataFrame(list(data))
    df.rename(columns={"timestamp": "Waktu", "ppm": "PPM", "temp": "Temp", "humi": "Humidity"}, inplace=True)

    # Simpan ke folder media
    dataset_path = settings.MEDIA_ROOT / 'data'
    dataset_path.mkdir(parents=True, exist_ok=True)
    csv_path = dataset_path / filename
    df.to_csv(csv_path, index=False)

    return redirect(reverse('fiturapp:uploadapp:file_list'))
