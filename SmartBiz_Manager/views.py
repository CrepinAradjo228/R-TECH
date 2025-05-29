from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm

from .models import Article

from django.shortcuts import render
from .models import Article, Vente, Facture
from django.contrib import messages
from datetime import date
from decimal import Decimal
from django.utils import timezone





# Create your views here.
def home(request):
    return render(request, 'index.html')

def index(request):
    articles = Article.objects.all()
    return render(request, 'gestion_vente/index.html', {'articles': articles})


#### debut vue des paniers
    #vue de l'affichage du panier




def afficher_panier(request):
    panier = request.session.get('panier', {})
    total = sum(item['quantite'] * float(item['prix_unitaire']) for item in panier.values())
    return render(request, 'vente/panier.html', {'panier': panier, 'total': total})

# Ajouter un article au panier
def ajouter_au_panier(request, article_id):
    panier = request.session.get('panier', {})

    article = get_object_or_404(Article, id=article_id)
    if str(article_id) in panier:
        panier[str(article_id)]['quantite'] += 1
    else:
        panier[str(article_id)] = {
            'quantite': 1,
            'prix_unitaire': str(article.prix_unitaire)
        }

    request.session['panier'] = panier
    messages.success(request, f"Article {article.nom} ajouté au panier.")
    return redirect('ventes')


# Afficher le panier
def afficher_panier(request):
    panier = request.session.get('panier', {})
    total = 0

    for item in panier.values():
        item['total'] = round(Decimal(item['quantite']) * Decimal(item['prix_unitaire']), 2)
        total += item['total']

    return render(request, 'vente/panier.html', {'panier': panier, 'total': total})

# Modifier la quantité d’un article
def modifier_quantite_panier(request, article_id):
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        panier = request.session.get('panier', {})

        if str(article_id) in panier:
            panier[str(article_id)]['quantite'] = quantite
            request.session['panier'] = panier
            messages.success(request, "Quantité mise à jour.")
    return redirect('afficher_panier')

# Supprimer un article du panier
def supprimer_du_panier(request, article_id):
    panier = request.session.get('panier', {})
    if str(article_id) in panier:
        del panier[str(article_id)]
        request.session['panier'] = panier
        messages.success(request, "Article supprimé du panier.")
    return redirect('afficher_panier')

# Valider la vente et créer une facture
def valider_vente(request):
    panier = request.session.get('panier', {})
    if not panier:
        messages.error(request, "Votre panier est vide.")
        return redirect('afficher_panier')

    vente = Vente.objects.create(
        nombreArticles=sum(item['quantite'] for item in panier.values()),
        prixTotal=sum(Decimal(item['prix_unitaire']) * item['quantite'] for item in panier.values()),
        date=date.today()
    )

    for article_id, item in panier.items():
        article = get_object_or_404(Article, id=int(article_id))
        vente.articles.add(article)
        # Mise à jour du stock
        article.quantite_stock -= item['quantite']
        article.save()

    vente.save()

    facture = Facture.objects.create(
        numeroFacture=f"FACT-{vente.id:05d}",
        nomClient="Client",
        telephoneClient="00000000",
        dateEmission=date.today(),
        vente=vente,
        montant=vente.prixTotal,
        modePaiement="Espèces"
    )

    request.session['panier'] = {}
    messages.success(request, f"Vente enregistrée. Facture n° {facture.numeroFacture} générée.")
    return redirect('index')
#fin des vues Ventes 


def dashboard(request):
    return render(request, 'gestion_vente/dashboard_vente.html')



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


