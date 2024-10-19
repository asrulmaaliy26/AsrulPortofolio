from django.shortcuts import render


def index(request):
    context = {
        'Judul': 'Beranda Portfolio',
        'Heading': 'Selamat datang',
    }
    return render(request, 'index.html', context)

def template(request):
    context = {
        'Judul': 'Template & Fitur - fitur',
        'Heading': "Selamat datang di Asrul's Template",
    }
    return render(request, 'template.html', context)
