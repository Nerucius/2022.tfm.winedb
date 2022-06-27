from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    return render(request, 'web/index.html')

def wine_list(request):
    return render(request, 'web/wine_list.html')

def wine_detail(request, wine_id):
    return render(request, 'web/wine_detail.html', {'wine_id': wine_id})

def find_wine(request):
    return render(request, 'web/find_wine.html')
