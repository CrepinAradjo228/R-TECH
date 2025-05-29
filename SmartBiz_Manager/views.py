from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article

# Create your views here.
def home(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'gestion_vente/dashboard_vente.html')

def ventes(request):
    return render(request, 'gestion_vente/index.html')

def articles(request):
    articles = Article.objects.all()
    return render(request, 'gestion_articles/index.html', {'articles': articles})

def ajout_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Cette ligne est ajoutée pour sauvegarder les données
            return redirect('articles')
    else:
        form = ArticleForm()
    return render(request, 'gestion_articles/ajout_article.html', {'form': form})


def analyse(request):
       
    return render(request, 'analyse/dashboard.html')

def modifier_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'gestion_articles/modifier_article.html', {'form': form, 'article': article})

def supprimer_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('articles')
    return render(request, 'gestion_articles/supprimer_article.html', {'article': article})

