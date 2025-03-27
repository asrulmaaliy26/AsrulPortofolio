import random
from django.http import JsonResponse
from .models import SensorSmartACData

is_receiving = True  # Variabel global untuk mengontrol penerimaan data

def process_sensor_data(request, allow_extra_fields=False):
    """ Fungsi helper untuk memproses dan menyimpan data sensor """
    global is_receiving
    if not is_receiving:
        return JsonResponse({"message": "Penerimaan data dihentikan"}, status=200)

    if request.method == "POST":
        try:
            random_value = random.randint(1, 100)
            
            data = request.POST
            ppm, temp, humi, tempout, humiout, tempac, modeac = data.get("ppm"), data.get("temp"), data.get("humi"), data.get("tempout"), data.get("humiout"), data.get("tempac"), data.get("modeac")
            
            
            if not all([ppm, temp, humi, tempout, humiout, tempac, modeac]):
                return JsonResponse({"error": "Data utama tidak lengkap"}, status=400)
            
            hasilpred = random_value
            extra_fields = {}
            if allow_extra_fields:
                extra_fields["tempac"] = data.get("tempac", None)
                extra_fields["modeac"] = data.get("modeac", None)
            
            SensorSmartACData.objects.create(ppm=ppm, temp=temp, humi=humi, tempout=tempout, humiout=humiout, tempac=tempac, modeac=modeac, hasilpred=random_value, **extra_fields)
            return JsonResponse({"message": "Data berhasil diproses", "nilai_random": random_value}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Kesalahan server: {str(e)}"}, status=500)
    
    return JsonResponse({"error": "Metode tidak diperbolehkan"}, status=405)
