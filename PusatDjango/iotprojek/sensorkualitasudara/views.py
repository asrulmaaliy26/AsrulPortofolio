from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random

# Global Constants
DATA_LOG_PATH = Path("iotprojek/sensorkualitasudara/data/data.log")
DATA_TEMP_LOG_PATH = Path("iotprojek/sensorkualitasudara/data/datatemp.log")
ML_PROJECT_PATH = Path("mlprojek/data/")
is_receiving = True

def index(request):
    return render(request, "sensor/index.html")

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

def get_temp_log(request):
    log_data = read_file_content(DATA_TEMP_LOG_PATH).splitlines()
    return render(request, "sensor/view_temp_log.html", {"log_data": log_data})

def view_temp_log(request):
    DATA_TEMP_LOG_PATH.write_text(DATA_LOG_PATH.read_text(), encoding='utf-8')
    log_data = read_file_content(DATA_TEMP_LOG_PATH).splitlines()
    return render(request, "sensor/view_temp_log.html", {"log_data": log_data})

def clean_data_line(line):
    parts = [p.split(": ")[-1] for p in line.strip().split(" | ")]
    return parts if len(parts) == 4 else None

def export_csv(request):
    return export_file(request, "csv")

def export_excel(request):
    return export_file(request, "excel")

def export_pdf(request):
    return export_file(request, "pdf")

def export_file(request, file_type):
    try:
        data = DATA_TEMP_LOG_PATH.read_text(encoding='utf-8').splitlines()
        clean_data = [clean_data_line(line) for line in data if clean_data_line(line)]
        if not clean_data:
            return HttpResponse("Tidak ada data untuk diekspor.", content_type="text/plain")
        
        df = pd.DataFrame(clean_data, columns=["Waktu", "PPM", "Temp", "Humidity"])
        file_extension = "xlsx" if file_type == "excel" else file_type
        response = HttpResponse(content_type=get_content_type(file_type))
        response['Content-Disposition'] = f'attachment; filename="data_log.{file_extension}"'
        
        if file_type == "csv":
            df.to_csv(response, index=False)
        elif file_type == "excel":
            df.to_excel(response, index=False, engine="openpyxl")
        elif file_type == "pdf":
            generate_pdf(response, data)
        
        return response
    except FileNotFoundError:
        return HttpResponse("File datatemp.log tidak ditemukan.", content_type="text/plain")

def get_content_type(file_type):
    return {
        "csv": "text/csv",
        "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "pdf": "application/pdf"
    }[file_type]

def generate_pdf(response, data):
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica", 12)
    y_position = height - 40
    for line in data:
        if y_position < 40:
            p.showPage()
            p.setFont("Helvetica", 12)
            y_position = height - 40
        p.drawString(50, y_position, line.strip())
        y_position -= 20
    p.save()

def upload_dataset(request):
    """ Export data ke CSV dengan nama file yang diinput user """
    try:
        if request.method != "POST":
            return HttpResponse("Metode tidak diizinkan.", status=405)

        filename = request.POST.get("filename", "").strip()
        if not filename:
            filename = "dataset.csv"  # Default jika tidak diisi
        elif not filename.lower().endswith(".csv"):  
            filename += ".csv"

        # Membaca data dari file
        try:
            with open(DATA_TEMP_LOG_PATH, "r") as file:
                data = file.readlines()
        except FileNotFoundError:
            return HttpResponse("File datatemp.log tidak ditemukan.", content_type="text/plain")

        if not data:
            return HttpResponse("Tidak ada data untuk diekspor.", content_type="text/plain")

        # Bersihkan data dan ambil hanya angka
        clean_data = [clean_data_line(line) for line in data if clean_data_line(line)]

        # Simpan ke CSV
        df = pd.DataFrame(clean_data, columns=["Waktu", "PPM", "Temp", "Humidity"])
        
        # Simpan ke folder dataset sesuai pilihan
        dataset_path = Path(settings.MEDIA_ROOT) / 'data'
        dataset_path.mkdir(parents=True, exist_ok=True)  
        csv_path = dataset_path / filename  # Simpan file dengan nama yang diinput user
        df.to_csv(csv_path, index=False)  
        
        return redirect(reverse('fiturapp:uploadapp:file_list'))
    except Exception as e:
        return HttpResponse(f"Terjadi kesalahan: {str(e)}", content_type="text/plain")