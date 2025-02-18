
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from PIL import Image
from pikepdf import Pdf
from io import BytesIO
from docx import Document
import base64
from .forms import ImageUploadForm, FileUploadForm

class ExampleView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'compress/index.html', {"message": "Hello, this is a class-based view!"})

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'compress/index.html')

class ImageUploadView(FormView):
    template_name = 'compress/upload_image.html'
    form_class = ImageUploadForm

    def form_valid(self, form):
        image = form.cleaned_data['image']
        quality = form.cleaned_data['quality']
        
        # Kompresi gambar
        img = Image.open(image)
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        compressed_image_io = BytesIO()
        img.save(compressed_image_io, format='JPEG', quality=quality)
        compressed_image_io.seek(0)
        
        # Konversi ke base64 untuk ditampilkan
        encoded_img = base64.b64encode(compressed_image_io.getvalue()).decode('utf-8')

        # Konversi ukuran file
        def convert_size(size):
            return f"{round(size / (1024 * 1024), 2)} MB" if size >= 1024 * 1024 else f"{round(size / 1024, 2)} KB"
        
        context = {
            'form': form,
            'compressed_img': encoded_img,
            'original_size': convert_size(image.size),
            'compressed_size': convert_size(len(compressed_image_io.getvalue())),
        }
        return render(self.request, self.template_name, context)

class FileUploadView(FormView):
    template_name = 'compress/upload_file.html'
    form_class = FileUploadForm

    def form_valid(self, form):
        file = form.cleaned_data['file']
        file_name = file.name.lower()
        compressed_file_io = None
        
        if file_name.endswith('.pdf'):
            with Pdf.open(file) as pdf:
                compressed_file_io = BytesIO()
                pdf.save(compressed_file_io, compress_streams=True)
        elif file_name.endswith('.docx'):
            doc = Document(file)
            compressed_file_io = BytesIO()
            doc.save(compressed_file_io)
        
        if compressed_file_io:
            compressed_size_kb = round(len(compressed_file_io.getvalue()) / 1024, 2)
            encoded_file = base64.b64encode(compressed_file_io.getvalue()).decode('utf-8')
            
            context = {
                'form': form,
                'compressed_file': encoded_file,
                'original_size': round(file.size / 1024, 2),
                'compressed_size': compressed_size_kb,
                'file_type': file_name.split('.')[-1],
            }
            return render(self.request, self.template_name, context)

        return super().form_invalid(form)
