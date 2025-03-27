import datetime
from pathlib import Path
from django.shortcuts import render
from fitur.scraping.views import get_bmkg_data
from mlprojek.prediksi.views import get_hasil_prediksi_data

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorSmartACData

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
    """ Menerima data dari sensor dan menyimpannya ke database """
    global is_receiving
    if not is_receiving:
        return JsonResponse({"message": "Penerimaan data dihentikan"}, status=200)

    if request.method == "POST":
        try:
            random_value = random.randint(1, 100)
            
            data = request.POST
            ppm = data.get("ppm")
            temp = data.get("temp")
            humi = data.get("humi")
            tempout = data.get("tempout")
            humiout = data.get("humiout")
            tempac = data.get("tempac")
            modeac = data.get("modeac")
            
            if not all([ppm, temp, humi, tempout, humiout, tempac, modeac]):
                return JsonResponse({"error": "Data tidak lengkap"}, status=400)

            # Simpan ke database
            hasilpred = random_value  # Bisa diganti dengan hasil prediksi sesungguhnya
            SensorSmartACData.objects.create(
                ppm=ppm, temp=temp, humi=humi, tempout=tempout, 
                humiout=humiout, tempac=tempac, modeac=modeac, hasilpred=hasilpred
            )

            return JsonResponse({
                "message": f"Data berhasil diterima, nilai random: {random_value}",
                "nilai_random": random_value
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Hanya menerima POST"}, status=405)

def get_data_ac(request):
    """ Mengambil data dari database dan mengembalikannya dalam format JSON """
    data = SensorSmartACData.objects.order_by('-timestamp').values("timestamp", "ppm", "temp", "humi", "tempout", "humiout", "tempac", "modeac", "hasilpred")
    return JsonResponse(list(data), safe=False)