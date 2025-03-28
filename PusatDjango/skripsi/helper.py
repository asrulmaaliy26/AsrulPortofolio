import random
from django.http import JsonResponse
from .models import SensorSmartACData

is_receiving = True  # Variabel global untuk mengontrol penerimaan data

def process_sensor_data(request):
    """ Fungsi helper untuk memproses dan menyimpan data sensor """
    global is_receiving
    if not is_receiving:
        return JsonResponse({"message": "Penerimaan data dihentikan"}, status=200)

    if request.method == "POST":
        try:
            random_value = random.randint(1, 100)
            
            data = request.POST
            tempout = data.get("tempout")
            humiout = data.get("humiout")
            tempac = data.get("tempac")
            modeac = data.get("modeac")
            
            if not all([tempout, humiout, tempac, modeac]):
                return JsonResponse({"error": "Data utama tidak lengkap"}, status=400)
            
            SensorSmartACData.objects.create(
                tempout=tempout, 
                humiout=humiout, 
                tempac=tempac, 
                modeac=modeac, 
                hasilpred=random_value)
            return JsonResponse({"message": "Data berhasil diproses", "nilai_random": random_value}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Kesalahan server: {str(e)}"}, status=500)
    
    return JsonResponse({"error": "Metode tidak diperbolehkan"}, status=405)
