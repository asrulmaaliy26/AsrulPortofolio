import requests
import pandas as pd
import pvlib
from datetime import datetime
import pytz
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'skripsi/index.html')

def dataapibmkg(request):
     # Lokasi geografis: Sukun, Malang, Jawa Timur
    latitude = -8.106735
    longitude = 112.027246

    # Mengambil data dari API BMKG
    url = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=35.04.11.2011"
    response = requests.get(url)
    
    # Pastikan response sukses
    if response.status_code != 200:
        return render(request, 'skripsi/dataapibmkg.html', {'error': 'Gagal mengambil data cuaca dari BMKG'})

    data = response.json()
    cuaca_data = data.get('data', [])[0].get('cuaca', [])

    cuaca_dict = {}

    for entry in cuaca_data:
        for weather in entry:
            # Konversi dari format ISO 8601 ke datetime Python
            utc_time = datetime.strptime(weather['datetime'], "%Y-%m-%dT%H:%M:%SZ")

            # Konversi ke zona waktu Asia/Jakarta
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Jakarta'))

            # Format tanggal dan waktu untuk tampilan
            tanggal = local_time.strftime("%Y-%m-%d")
            waktu = local_time.strftime("%H:%M")

            # Hitung posisi matahari
            solar_position = pvlib.solarposition.get_solarposition(local_time, latitude, longitude)
            elevation = solar_position['elevation'].iloc[0]
            azimuth = solar_position['azimuth'].iloc[0]

            # Simpan data berdasarkan tanggal
            if tanggal not in cuaca_dict:
                cuaca_dict[tanggal] = []

            cuaca_dict[tanggal].append({
                'waktu': waktu,
                'suhu': weather['t'],
                'kelembapan': weather['hu'],
                'kecepatan_angin': weather['ws'],
                'arah_angin': weather['wd'],
                'deskripsi_cuaca': weather['weather_desc'],
                'elevasi_matahari': elevation,
                'azimut_matahari': azimuth
            })

    # Kirim data ke template
    return render(request, 'skripsi/dataapibmkg.html', {'cuaca_dict': cuaca_dict})


def datascrapingbmkg(request):
     # Lokasi geografis: Sukun, Malang, Jawa Timur
    latitude = -8.106735
    longitude = 112.027246

    # Mengambil data dari API BMKG
    url = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=35.04.11.2011"
    response = requests.get(url)
    
    # Pastikan response sukses
    if response.status_code != 200:
        return render(request, 'skripsi/datascrapingbmkg.html', {'error': 'Gagal mengambil data cuaca dari BMKG'})

    data = response.json()
    cuaca_data = data.get('data', [])[0].get('cuaca', [])

    cuaca_dict = {}

    for entry in cuaca_data:
        for weather in entry:
            # Konversi dari format ISO 8601 ke datetime Python
            utc_time = datetime.strptime(weather['datetime'], "%Y-%m-%dT%H:%M:%SZ")

            # Konversi ke zona waktu Asia/Jakarta
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Jakarta'))

            # Format tanggal dan waktu untuk tampilan
            tanggal = local_time.strftime("%Y-%m-%d")
            waktu = local_time.strftime("%H:%M")

            # Hitung posisi matahari
            solar_position = pvlib.solarposition.get_solarposition(local_time, latitude, longitude)
            elevation = solar_position['elevation'].iloc[0]
            azimuth = solar_position['azimuth'].iloc[0]

            # Simpan data berdasarkan tanggal
            if tanggal not in cuaca_dict:
                cuaca_dict[tanggal] = []

            cuaca_dict[tanggal].append({
                'waktu': waktu,
                'suhu': weather['t'],
                'kelembapan': weather['hu'],
                'kecepatan_angin': weather['ws'],
                'arah_angin': weather['wd'],
                'deskripsi_cuaca': weather['weather_desc'],
                'elevasi_matahari': elevation,
                'azimut_matahari': azimuth
            })

    # Kirim data ke template
    return render(request, 'skripsi/datascrapingbmkg.html', {'cuaca_dict': cuaca_dict})
