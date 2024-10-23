from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageUploadForm
from PIL import Image
from io import BytesIO
import base64

def index(request):
    return render(request, 'fiturapp/index.html')

def compress_image(image, quality):
    # Membuka gambar dengan PIL
    img = Image.open(image)

    # Cek jika gambar dalam mode 'RGBA' (dengan transparansi), konversi ke 'RGB'
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Kompresi gambar
    compressed_image_io = BytesIO()
    img.save(compressed_image_io, format='JPEG', quality=quality)
    compressed_image_io.seek(0)  # Mengatur ulang posisi pointer ke awal

    return compressed_image_io

def upload_image(request):
    judul = 'Upload Image to compress'
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            quality = form.cleaned_data['quality']

            # Kompresi gambar
            compressed_image_io = compress_image(image, quality)

            # Konversi gambar yang sudah dikompres ke base64 untuk ditampilkan tanpa menyimpan ke server
            encoded_img = base64.b64encode(compressed_image_io.getvalue()).decode('utf-8')

            # Dapatkan ukuran file asli (dalam byte) dan konversi ke KB atau MB
            original_size = image.size
            compressed_size = len(compressed_image_io.getvalue())

            # Fungsi untuk mengonversi ukuran byte ke KB atau MB
            def convert_size(size):
                if size >= 1024 * 1024:  # Jika ukuran >= 1 MB
                    return f"{round(size / (1024 * 1024), 2)} MB"
                else:  # Jika ukuran < 1 MB
                    return f"{round(size / 1024, 2)} KB"

            # Konversi ukuran asli dan terkompresi
            original_size_str = convert_size(original_size)
            compressed_size_str = convert_size(compressed_size)

            context = {
                'judul' : judul,
                'form': form,
                'compressed_img': encoded_img,
                'original_size': original_size_str,  # Ukuran asli dalam KB atau MB
                'compressed_size': compressed_size_str,  # Ukuran terkompresi dalam KB atau MB
            }
            return render(request, 'fiturapp/upload_image.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'fiturapp/upload_image.html', {'form': form, 'judul': judul})
