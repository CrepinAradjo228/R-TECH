from django.shortcuts import render, redirect
from .forms import ArticleForm
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'gestion_vente/dashboard_vente.html')

def ventes(request):
    return render(request, 'gestion_vente/index.html')

def articles(request):
    return render(request, 'gestion_articles/index.html')

def ajout_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Cette ligne est ajoutée pour sauvegarder les données
            return redirect('articles')
    else:
        form = ArticleForm()
    return render(request, 'gestion_articles/ajout_article.html', {'form': form})
