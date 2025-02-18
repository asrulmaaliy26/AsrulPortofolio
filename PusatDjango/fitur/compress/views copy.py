from django.shortcuts import render
from django.views import View
from PIL import Image
from pikepdf import Pdf
from io import BytesIO
from docx import Document
import base64
from .forms import ImageUploadForm, FileUploadForm

def index(request):
    return render(request, 'compress/index.html')

class ExampleView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'compress/index.html', {"message": "Hello, this is a class-based view!"})
    
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
            return render(request, 'compress/upload_image.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'compress/upload_image.html', {'form': form, 'judul': judul})



#compress PDF



def compress_pdf(pdf_file):
    """Fungsi untuk kompresi file PDF"""
    with Pdf.open(pdf_file) as pdf:
        compressed_pdf_io = BytesIO()
        pdf.save(compressed_pdf_io, compress_streams=True)
        return compressed_pdf_io
    
def compress_docx(docx_file):
    """Fungsi sederhana untuk 'mengompresi' file DOCX dengan mengurangi gambar"""
    doc = Document(docx_file)
    compressed_docx_io = BytesIO()
    doc.save(compressed_docx_io)
    return compressed_docx_io

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            file_name = file.name.lower()

            compressed_file_io = None
            original_size_kb = round(file.size / 1024, 2)

            if file_name.endswith('.pdf'):
                # Kompres PDF
                compressed_file_io = compress_pdf(file)
            elif file_name.endswith('.docx'):
                # 'Kompres' file DOCX
                compressed_file_io = compress_docx(file)

            if compressed_file_io:
                compressed_size_kb = round(len(compressed_file_io.getvalue()) / 1024, 2)
                encoded_file = base64.b64encode(compressed_file_io.getvalue()).decode('utf-8')

                context = {
                    'form': form,
                    'compressed_file': encoded_file,
                    'original_size': original_size_kb,
                    'compressed_size': compressed_size_kb,
                    'file_type': file_name.split('.')[-1],  # Mendapatkan ekstensi file
                }
                return render(request, 'compress/upload_file.html', context)

    else:
        form = FileUploadForm()

    return render(request, 'compress/upload_file.html', {'form': form})