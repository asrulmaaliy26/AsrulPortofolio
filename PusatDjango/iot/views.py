from django.shortcuts import render
from django.views import View

def index(request):
    return render(request, 'iot/index.html')

class ExampleView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'iot/index.html', {"message": "Hello, this is a class-based view! IOT"})
    