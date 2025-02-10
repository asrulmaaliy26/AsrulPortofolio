import pytz
import pvlib
import requests
from datetime import datetime
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'scraping/index.html')

LATITUDE = -8.106735
LONGITUDE = 112.027246

def get_bmkg_data(request=None):
    """Mengambil dan memproses data cuaca dari API BMKG"""
    url = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=35.04.11.2011"
    response = requests.get(url)

    if response.status_code != 200:
        return {'error': 'Gagal mengambil data cuaca dari BMKG'}

    data = response.json()
    cuaca_data = data.get('data', [])[0].get('cuaca', [])

    cuaca_dict = {}

    for entry in cuaca_data:
        for weather in entry:
            # Konversi dari format ISO 8601 ke datetime Python
            utc_time = datetime.strptime(weather['datetime'], "%Y-%m-%dT%H:%M:%SZ")
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Jakarta'))

            # Format tanggal dan waktu untuk tampilan
            tanggal = local_time.strftime("%Y-%m-%d")
            waktu = local_time.strftime("%H:%M")

            # Hitung posisi matahari
            solar_position = pvlib.solarposition.get_solarposition(local_time, LATITUDE, LONGITUDE)
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

    return {'cuaca_dict': cuaca_dict}

def scrapingbmkg(request):
    """View untuk menampilkan data cuaca BMKG"""
    cuaca_dict = get_bmkg_data()
    
    # Cek jika terjadi error saat mengambil data
    if 'error' in cuaca_dict:
        return render(request, 'scraping/scrapingbmkg.html', {'error': cuaca_dict['error']})

    return render(request, 'scraping/scrapingbmkg.html', cuaca_dict)
