from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm

from .models import Article

from django.shortcuts import render
from .models import Article, Vente, Facture,LigneCommande
from django.contrib import messages
from datetime import date
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models import Sum, Count
from SmartBiz_Manager.models import Vente, LigneCommande, Article
import json
import datetime





# Create your views here.
def home(request):
    return render(request, 'index.html')

def index(request):
    articles = Article.objects.all()
    ventes = Vente.objects.all()
    
    # Calcul des statistiques
    chiffre_affaire = ventes.aggregate(total=Sum('prixTotal'))['total'] or 0.0
    total_ventes = ventes.aggregate(total=Sum('prixTotal'))['total'] or 0.0
    today = now().date()
    ventes_du_jour = Vente.objects.filter(date=today).count()
    
    # Préparation des données pour le graphique de stock
    for article in articles:
        # Calcul du pourcentage de stock (pour la barre de progression)
        article.stock_percentage = min(100, max(0, article.quantite_stock))  # Limite entre 0 et 100
        
        # Détermination de la couleur en fonction du niveau de stock
        if article.quantite_stock <= 0:
            article.stock_status = "danger"
            article.stock_message = "Rupture de stock"
        elif article.quantite_stock < 10:  # Seuil d'alerte
            article.stock_status = "warning"
            article.stock_message = f"{article.quantite_stock} restant(s)"
        else:
            article.stock_status = "success"
            article.stock_message = f"{article.quantite_stock} en stock"
    
    return render(request, 'gestion_vente/index.html', {
        'articles': articles,
        'ventes': ventes,
        'chiffre_affaire': chiffre_affaire,
        'total_ventes': total_ventes,
        'ventes_du_jour': ventes_du_jour,
        'now': now()
    })
#### debut vue des paniers
    #vue de l'affichage du panier






# # Ajouter un article au panier
# def ajouter_au_panier(request, article_id):
#     panier = request.session.get('panier', {})
#     article = get_object_or_404(Article, id=article_id)

#     if str(article_id) in panier:
#         panier[str(article_id)]['quantite'] += 1
#     else:
#         panier[str(article_id)] = {
#             'quantite': 1,
#             'prix_unitaire': str(article.prix_unitaire),
#             'nom': article.nom,
#             'id': article.id  # Inclure l'ID si nécessaire
#         }

#     request.session['panier'] = panier
#     messages.success(request, f"Article {article.nom} ajouté au panier.")
#     return redirect('ventes')


# # Afficher le panier
# def afficher_panier(request):
#     panier = request.session.get('panier', {})
#     total = 0.0
#     articles = {}  # Dictionnaire pour stocker les articles

#     # Récupérer tous les articles en une seule requête
#     article_ids = panier.keys()
#     for article_id in article_ids:
#         article = Article.objects.get(id=article_id)  # Récupérer l'article
#         articles[article_id] = article  # Stocker l'article par son ID

#     # Calculer le total du panier
#     for article_id, details in panier.items():
#         total_article = details['quantite'] * float(details['prix_unitaire'])
#         details['total'] = total_article
#         total += total_article

#     return render(request, 'gestion_vente/panier.html', {'panier': panier, 'total': total, 'articles': articles})

# # Modifier la quantité d’un article
# def modifier_quantite_panier(request, article_id):
#     if request.method == 'POST':
#         quantite = int(request.POST.get('quantite', 1))
#         panier = request.session.get('panier', {})

#         if str(article_id) in panier:
#             panier[str(article_id)]['quantite'] = quantite
#             request.session['panier'] = panier
#             messages.success(request, "Quantité mise à jour.")
#     return redirect('afficher_panier')

# # Supprimer un article du panier
# def supprimer_du_panier(request, article_id):
#     panier = request.session.get('panier', {})
#     if str(article_id) in panier:
#         del panier[str(article_id)]
#         request.session['panier'] = panier
#         messages.success(request, "Article supprimé du panier.")
#     return redirect('afficher_panier')

# # Valider la vente et créer une facture
# def valider_vente(request):
#     panier = request.session.get('panier', {})
#     if not panier:
#         messages.error(request, "Votre panier est vide.")
#         return redirect('afficher_panier')

#     vente = Vente.objects.create(
#         nombreArticles=sum(item['quantite'] for item in panier.values()),
#         prixTotal=sum(Decimal(item['prix_unitaire']) * item['quantite'] for item in panier.values()),
#         date=date.today()
#     )

#     for article_id, item in panier.items():
#         article = get_object_or_404(Article, id=int(article_id))
#         vente.articles.add(article)
#         # Mise à jour du stock
#         article.quantite_stock -= item['quantite']
#         article.save()

#     vente.save()

#     facture = Facture.objects.create(
#         numeroFacture=f"FACT-{vente.id:05d}",
#         nomClient="Client",
#         telephoneClient="00000000",
#         dateEmission=date.today(),
#         vente=vente,
#         montant=vente.prixTotal,
#         modePaiement="Espèces"
#     )

#     request.session['panier'] = {}
#     messages.success(request, f"Vente enregistrée. Facture n° {facture.numeroFacture} générée.")
#     return redirect('index')
# #fin des vues Ventes


def ajouter_au_panier(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    panier = request.session.get('panier', {})
    
    if str(article_id) in panier:
        panier[str(article_id)]['quantite'] += 1
    else:
        panier[str(article_id)] = {
            'nom': article.nom,  # Assurez-vous que ce champ existe
            'prix_unitaire': str(article.prix_unitaire),  # Conversion en string si nécessaire
            'quantite': 1,
        }
    
    request.session['panier'] = panier
    return redirect('ventes')

def supprimer_du_panier(request, article_id):
    panier = request.session.get('panier', {})
    article_id = str(article_id)  # Conversion en string pour cohérence
    
    if article_id in panier:
        del panier[article_id]
        request.session['panier'] = panier
        request.session.modified = True  # Force la sauvegarde de la session
    
    return redirect('afficher_panier')

def vider_panier(request):
    if 'panier' in request.session:
        del request.session['panier']
        messages.success(request, "Votre panier a été vidé.")
    return redirect('afficher_panier')

def modifier_quantite(request, article_id):
    if request.method == 'POST' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        panier = request.session.get('panier', {})
        nouvelle_quantite = int(request.POST.get('quantite', 1))
        
        if article_id in panier and nouvelle_quantite > 0:
            panier[article_id]['quantite'] = nouvelle_quantite
            panier[article_id]['total'] = nouvelle_quantite * float(panier[article_id]['prix_unitaire'])
            request.session['panier'] = panier
            
            # Calculer le nouveau total du panier
            total_panier = sum(float(item['total']) for item in panier.values())
            
            return JsonResponse({
                'success': True,
                'quantite': nouvelle_quantite,
                'total_article': panier[article_id]['total'],
                'total_panier': total_panier
            })
        elif nouvelle_quantite <= 0:
            return JsonResponse({
                'success': False,
                'message': 'La quantité doit être supérieure à zéro.'
            }, status=400)
    
    return JsonResponse({'success': False}, status=400)

def afficher_panier(request):
    panier = request.session.get('panier', {})
    total = 0.0

    for article_id, details in panier.items():
        # Vérifiez toutes les clés nécessaires
        if all(key in details for key in ['quantite', 'prix_unitaire', 'nom']):
            total_article = details['quantite'] * float(details['prix_unitaire'])
            details['total'] = total_article
            total += total_article
        else:
            # Gérer le cas où des informations sont manquantes
            details['nom'] = details.get('nom', 'Produit non disponible')
            details['total'] = 0.0

    return render(request, 'gestion_vente/panier.html', {'panier': panier, 'total': total})

def valider_vente(request):
    panier = request.session.get('panier', {})
    
    if not panier:
        return redirect('afficher_panier')
    
    try:
        # Calcul des totaux
        total_articles = sum(item['quantite'] for item in panier.values())
        prix_total = sum(float(item['prix_unitaire']) * item['quantite'] for item in panier.values())
        
        # Création de la vente (avec vos champs existants)
        vente = Vente.objects.create(
            nombreArticles=total_articles,
            prixTotal=prix_total,
            date=timezone.now().date()  # Utilise auto_now=True de votre modèle
        )
        
        # Ajout des articles (ManyToMany comme dans votre modèle)
        articles_ids = []
        for article_id, item in panier.items():
            article = Article.objects.get(pk=article_id)
            articles_ids.append(article.id)
            
            # Création des lignes de commande détaillées
            LigneCommande.objects.create(
                vente=vente,
                article=article,
                quantite=item['quantite'],
                prix_unitaire=item['prix_unitaire']
            )
            
            # Mise à jour du stock (optionnel)
            article.quantite_stock -= item['quantite']
            article.save()
        
        # Ajout des articles à la relation ManyToMany existante
        vente.articles.set(articles_ids)
        
        # Nettoyage du panier
        del request.session['panier']
        request.session.modified = True
        
        return redirect('detail_vente', vente_id=vente.id)
    
    except Exception as e:
        print(f"Erreur validation: {str(e)}")
        return redirect('afficher_panier')

def detail_vente(request, vente_id):
    vente = get_object_or_404(Vente, pk=vente_id)
    lignes = vente.lignes_commande.all().select_related('article')
    
    context = {
        'vente': vente,
        'lignes': lignes,
        'total': sum(ligne.total_ligne for ligne in lignes)
    }
    return render(request, 'gestion_vente/detail_vente.html', context)

def supprimer_vente(request, vente_id):
    vente = get_object_or_404(Vente, pk=vente_id)
    
    if request.method == 'POST':
        # Supprimer les lignes de commande associées
        vente.lignes_commande.all().delete()
        # Supprimer la vente elle-même
        vente.delete()
        messages.success(request, "Vente supprimée avec succès.")
        return redirect('ventes')
    
    return render(request, 'gestion_vente/supprimer_vente.html', {'vente': vente})

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
    mois_selectionne = request.GET.get('mois', '')  # format attendu : 'YYYY-MM'

    # Récupération de toutes les ventes
    ventes = Vente.objects.all()

    # Extraction des mois disponibles dynamiquement au format 'YYYY-MM'
    mois_disponibles = ventes.dates('date', 'month').values_list('date', flat=True)
    mois_disponibles = sorted(set(dt.strftime('%Y-%m') for dt in mois_disponibles))

    # Filtrer selon le mois sélectionné
    if mois_selectionne and mois_selectionne in mois_disponibles:
        annee, mois = map(int, mois_selectionne.split('-'))
        ventes_filtrees = ventes.filter(date__year=annee, date__month=mois)
    else:
        ventes_filtrees = ventes

    # Calcul du chiffre d'affaires total (filtré)
    chiffre_affaire = ventes_filtrees.aggregate(total=Sum('prixTotal'))['total'] or Decimal('0')

    # Total articles vendus (filtré via lignes commandes liées aux ventes filtrées)
    ids_ventes = ventes_filtrees.values_list('id', flat=True)
    total_articles_vendus = LigneCommande.objects.filter(vente_id__in=ids_ventes).aggregate(total=Sum('quantite'))['total'] or 0

    # Nombre de clients (ventes uniques) dans la période
    total_clients = ventes_filtrees.count()

    # Bénéfice net : 30% du chiffre d'affaire
    benefice_net = chiffre_affaire * Decimal('0.3')

    # Ventes par mois (pour tous les mois disponibles, ou filtrés ? ici on fait tous)
    ventes_par_mois = {}
    for vente in ventes:
        mois_str = vente.date.strftime('%b %Y')  # ex: "Mai 2025"
        ventes_par_mois[mois_str] = ventes_par_mois.get(mois_str, 0) + float(vente.prixTotal)

    mois_labels = list(ventes_par_mois.keys())
    ventes_mensuelles = list(ventes_par_mois.values())

    # Top 5 produits (sur toutes les ventes, ou filtrées ? ici sur ventes filtrées)
    lignes = LigneCommande.objects.filter(vente_id__in=ids_ventes).values('article__nom').annotate(
        quantite_totale=Sum('quantite')
    ).order_by('-quantite_totale')[:5]

    produits = [ligne['article__nom'] for ligne in lignes]
    quantites = [ligne['quantite_totale'] for ligne in lignes]

    context = {
        'chiffre_affaire': chiffre_affaire,
        'total_articles_vendus': total_articles_vendus,
        'total_clients': total_clients,
        'benefice_net': benefice_net,

        'mois_labels': json.dumps(mois_labels),
        'ventes_mensuelles': json.dumps(ventes_mensuelles),

        'produits': json.dumps(produits),
        'quantites': json.dumps(quantites),

        'mois_selectionne': mois_selectionne,
        'mois_disponibles': mois_disponibles,
    }

    return render(request, 'analyse/dashboard.html', context)




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




