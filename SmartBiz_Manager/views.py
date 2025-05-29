from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'gestion_vente/dashboard_vente.html')

def ventes(request):
    return render(request, 'gestion_vente/index.html')
