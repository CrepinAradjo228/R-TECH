from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm

from .models import Article

from django.shortcuts import render
from .models import Article, Vente, Facture,LigneCommande, EcritureComptable
from django.contrib import messages
from datetime import date
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
from django.http import JsonResponse
from django.utils.timezone import now
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse
import csv
from django.db import transaction
from django.utils import timezone
import random
import string
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db import transaction
from .models import Vente, Article, LigneCommande, Facture, EcritureComptable
# from .tasks import send_facture_email  # Tâche pour envoyer la facture par email
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import render, redirect
from .models import Budget, Transaction, Department
from .forms import BudgetForm, TransactionForm, DepartmentForm
import json




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

# def valider_vente(request):
#     panier = request.session.get('panier', {})
    
#     if not panier:
#         return redirect('afficher_panier')
    
#     try:
#         # Calcul des totaux
#         total_articles = sum(item['quantite'] for item in panier.values())
#         prix_total = sum(float(item['prix_unitaire']) * item['quantite'] for item in panier.values())
        
#         # Création de la vente (avec vos champs existants)
#         vente = Vente.objects.create(
#             nombreArticles=total_articles,
#             prixTotal=prix_total,
#             date=timezone.now().date()  # Utilise auto_now=True de votre modèle
#         )
        
#         # Ajout des articles (ManyToMany comme dans votre modèle)
#         articles_ids = []
#         for article_id, item in panier.items():
#             article = Article.objects.get(pk=article_id)
#             articles_ids.append(article.id)
            
#             # Création des lignes de commande détaillées
#             LigneCommande.objects.create(
#                 vente=vente,
#                 article=article,
#                 quantite=item['quantite'],
#                 prix_unitaire=item['prix_unitaire']
#             )
            
#             # Mise à jour du stock (optionnel)
#             article.quantite_stock -= item['quantite']
#             article.save()
        
#         # Ajout des articles à la relation ManyToMany existante
#         vente.articles.set(articles_ids)
        
#         # Nettoyage du panier
#         del request.session['panier']
#         request.session.modified = True
        
#         return redirect('detail_vente', vente_id=vente.id)
    
#     except Exception as e:
#         print(f"Erreur validation: {str(e)}")
#         return redirect('afficher_panier')



def generate_numero_facture():
    # Génère un numéro de facture aléatoire (ex: FA20240520-ABCD)
    date_part = timezone.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase, k=4))
    return f"FA{date_part}-{random_part}"

# def valider_vente(request):
#     panier = request.session.get('panier', {})
#     if not panier:
#         return redirect('afficher_panier')
    
#     try:
#         with transaction.atomic():  # Transaction globale
#             # 1. Calcul des totaux
#             total_articles = sum(item['quantite'] for item in panier.values())
#             prix_total_ht = sum(float(item['prix_unitaire']) * item['quantite'] for item in panier.values())
#             tva = prix_total_ht * 0.20  # TVA 20%
#             prix_total_ttc = prix_total_ht + tva

#             # 2. Création de la vente
#             vente = Vente.objects.create(
#                 nombreArticles=total_articles,
#                 prixTotal=prix_total_ttc,
#                 date=timezone.now().date()
#             )

#             # 3. Création des lignes de commande + mise à jour stock
#             articles_ids = []
#             for article_id, item in panier.items():
#                 article = Article.objects.get(pk=article_id)
#                 articles_ids.append(article.id)
#                 LigneCommande.objects.create(
#                     vente=vente,
#                     article=article,
#                     quantite=item['quantite'],
#                     prix_unitaire=item['prix_unitaire']
#                 )
#                 article.quantite_stock -= item['quantite']
#                 article.save()

#             vente.articles.set(articles_ids)

#             # 4. Création de la facture (nouveau)
#             facture = Facture.objects.create(
#                 numeroFacture=generate_numero_facture(),
#                 nomClient=request.POST.get('nom_client', 'Client anonyme'),
#                 telephoneClient=request.POST.get('telephone_client', 'Non renseigné'),
#                 dateEmission=timezone.now().date(),
#                 vente=vente,
#                 montant=prix_total_ttc,
#                 modePaiement=request.POST.get('mode_paiement', 'ESPÈCES')  # ESPÈCES/CARTE/VIREMENT etc.
#             )

#             # 5. Écritures comptables (version améliorée)
#             # a) Écriture de vente (Client HT)
#             EcritureComptable.objects.create(
#                 journal='VT',
#                 date=timezone.now().date(),
#                 compte_debit='411000',  # Clients
#                 compte_credit='707000',  # Ventes
#                 montant=prix_total_ht,
#                 libelle=f"Facture {facture.numeroFacture} (HT)",
#                 vente=vente,
#                 facture=facture
#             )

#             # b) Écriture TVA
#             EcritureComptable.objects.create(
#                 journal='VT',
#                 date=timezone.now().date(),
#                 compte_debit='411000',  # Clients
#                 compte_credit='445710',  # TVA collectée
#                 montant=tva,
#                 libelle=f"TVA Facture {facture.numeroFacture}",
#                 vente=vente,
#                 facture=facture
#             )

#             # c) Si paiement immédiat (optionnel)
#             if facture.modePaiement != 'CREDIT':
#                 compte_paiement = '512000' if facture.modePaiement == 'VIREMENT' else '531000'  # Banque ou Caisse
#                 EcritureComptable.objects.create(
#                     journal='BQ',
#                     date=timezone.now().date(),
#                     compte_debit=compte_paiement,
#                     compte_credit='411000',  # Clients
#                     montant=prix_total_ttc,
#                     libelle=f"Paiement Facture {facture.numeroFacture}",
#                     vente=vente,
#                     facture=facture
#                 )

#             # 6. Nettoyage du panier
#             request.session['panier'] = {}
            
#             return redirect('visualiser_facture', facture_id=facture.id)

#     except Exception as e:
#         # Gestion d'erreur améliorée
#         return render(request, 'gestion_vente/erreur.html', {
#             'erreur': f"Erreur lors de la validation : {str(e)}"
#         }, status=500)




def valider_vente(request):
    panier = request.session.get('panier', {})
    if not panier:
        return redirect('afficher_panier')

    try:
        with transaction.atomic():
            # 1. Calcul des totaux
            total_articles = sum(item['quantite'] for item in panier.values())
            prix_total_ht = sum(float(item['prix_unitaire']) * item['quantite'] for item in panier.values())
            tva = prix_total_ht * 0.20  # TVA 20%
            prix_total_ttc = prix_total_ht + tva

            # 2. Création de la vente
            vente = Vente.objects.create(
                nombreArticles=total_articles,
                prixTotal=prix_total_ttc,
                date=timezone.now().date()
            )

            # 3. Création des lignes de commande + mise à jour stock
            for article_id, item in panier.items():
                article = Article.objects.get(pk=article_id)
                LigneCommande.objects.create(
                    vente=vente,
                    article=article,
                    quantite=item['quantite'],
                    prix_unitaire=item['prix_unitaire']
                )
                article.quantite_stock -= item['quantite']
                article.save()

            # 4. Création de la facture
            facture = Facture.objects.create(
                numeroFacture=generate_numero_facture(),
                nomClient=request.POST.get('nom_client', 'Client anonyme'),
                telephoneClient=request.POST.get('telephone_client', 'Non renseigné'),
                dateEmission=timezone.now().date(),
                vente=vente,
                montant=prix_total_ttc,
                modePaiement=request.POST.get('mode_paiement', 'ESPÈCES')
            )

            # 5. Écritures comptables
            create_ecritures_comptables(vente, facture, prix_total_ht, tva)

            # 6. Nettoyage du panier
            request.session['panier'] = {}

            # Envoi de la facture par email (tâche asynchrone)
            # send_facture_email.delay(facture.id)

            return redirect('visualiser_facture', facture_id=facture.id)

    except Exception as e:
        return render(request, 'gestion_vente/erreur.html', {
            'erreur': f"Erreur lors de la validation : {str(e)}"
        }, status=500)
        

def create_ecritures_comptables(vente, facture, prix_total_ht, tva):
    # a) Écriture de vente (Client HT)
    EcritureComptable.objects.create(
        journal='VT',
        date=timezone.now().date(),
        compte_debit='411000',  # Clients
        compte_credit='707000',  # Ventes
        montant=prix_total_ht,
        libelle=f"Facture {facture.numeroFacture} (HT)",
        vente=vente,
        facture=facture
    )

    # b) Écriture TVA
    EcritureComptable.objects.create(
        journal='VT',
        date=timezone.now().date(),
        compte_debit='411000',  # Clients
        compte_credit='445710',  # TVA collectée
        montant=tva,
        libelle=f"TVA Facture {facture.numeroFacture}",
        vente=vente,
        facture=facture
    )

    # c) Si paiement immédiat (optionnel)
    if facture.modePaiement != 'CREDIT':
        compte_paiement = '512000' if facture.modePaiement == 'VIREMENT' else '531000'
        EcritureComptable.objects.create(
            journal='BQ',
            date=timezone.now().date(),
            compte_debit=compte_paiement,
            compte_credit='411000',  # Clients
            montant=facture.montant,
            libelle=f"Paiement Facture {facture.numeroFacture}",
            vente=vente,
            facture=facture
        )

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




def visualiser_facture(request, vente_id):
    vente = get_object_or_404(Vente, pk=vente_id)
    facture = get_object_or_404(Facture, vente=vente)
    
    # Calcul des totaux pour le template
    context = {
        'facture': facture,
        'COMPANY_NAME': "Votre Entreprise",
        'COMPANY_ADDRESS': "123 Rue de Commerce\n75001 Paris",
        'COMPANY_SIRET': "123 456 789 00010",
        'COMPANY_PHONE': "+33 1 23 45 67 89",
        'COMPANY_IBAN': "FR76 1234 5678 9123 4567 8910 123",
        'COMPANY_LEGAL_MENTIONS': "SARL au capital de 10 000 € - RCS Paris 123 456 789 - TVA Intracommunautaire FR 12 123456789",
    }
    return render(request, 'gestion_vente/facture.html', context)



def export_facture_pdf(request, facture_id):
    facture = get_object_or_404(Facture, pk=facture_id)
    html_string = render_to_string('facture.html', {
        'facture': facture,
        # ... mêmes variables que la vue HTML ...
    })
    
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture.numeroFacture}.pdf"'
    return response


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





def cahier_comptable(request):
    # Récupération des paramètres de filtrage
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    journal = request.GET.get('journal')

    # Construction de la requête filtrée
    ecritures = EcritureComptable.objects.all().order_by('-date')
    
    if date_debut:
        ecritures = ecritures.filter(date__gte=date_debut)
    if date_fin:
        ecritures = ecritures.filter(date__lte=date_fin)
    if journal:
        ecritures = ecritures.filter(journal=journal)

    # Calcul des totaux
    total_debit = ecritures.aggregate(Sum('montant'))['montant__sum'] or 0
    total_credit = total_debit  # Partie double => toujours équilibré

    # Pagination (20 écritures par page)
    paginator = Paginator(ecritures, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'ecritures': page_obj,
        'total_debit': total_debit,
        'total_credit': total_credit,
    }
    return render(request, 'comptabilite/cahier_comptable.html', context)






def export_cahier_csv(request):
    # Récupère les mêmes filtres que la vue cahier_comptable
    ecritures = EcritureComptable.objects.all()
    
    # Crée la réponse HTTP avec le type CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cahier_comptable.csv"'
    
    writer = csv.writer(response, delimiter=';')
    # En-tête du CSV
    writer.writerow(['Date', 'Journal', 'Compte Débit', 'Compte Crédit', 'Libellé', 'Débit', 'Crédit'])
    
    # Données
    for ecriture in ecritures:
        writer.writerow([
            ecriture.date.strftime("%d/%m/%Y"),
            ecriture.get_journal_display(),
            ecriture.compte_debit,
            ecriture.compte_credit,
            ecriture.libelle,
            str(ecriture.montant).replace('.', ','),
            str(ecriture.montant).replace('.', ',')
        ])
    
    return response


def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'comptabilite/creer_departement.html', {'form': form})

def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'comptabilite/creer_budget.html', {'form': form})

def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'comptabilite/creer_transaction.html', {'form': form})

def budget_list(request):
    budgets = Budget.objects.select_related('department').all()  # Utiliser select_related pour optimiser les requêtes
    return render(request, 'comptabilite/budget_list.html', {'budgets': budgets})

def budget_summary(request):
    budgets = Budget.objects.all()
    budget_data = []
    for budget in budgets:
        total_transactions = Transaction.objects.filter(budget=budget).aggregate(Sum('amount'))['amount__sum'] or 0
        variance = budget.amount - total_transactions
        budget_data.append({
            'budget': budget,
            'total_transactions': total_transactions,
            'variance': variance,
        })
    return render(request, 'comptabilite/budget_summary.html', {'budget_data': budget_data})


def department_list(request):
    departments = Department.objects.all()
    return render(request, 'comptabilite/department_list.html', {'departments': departments})

def comptabilite (request):
    return render(request, 'comptabilite/index.html')


def transaction_list(request):
    # Récupérer le queryset de base
    queryset = Transaction.objects.select_related('budget__department')
    
    # Filtrage par budget
    budget_id = request.GET.get('budget')
    if budget_id:
        queryset = queryset.filter(budget_id=budget_id)
    
    # Filtrage par date
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    
    # Trier les transactions
    queryset = queryset.order_by('-date')
    
    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calcul du total
    total = queryset.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'transactions': page_obj,
        'total': total,
        'budgets': Budget.objects.all().select_related('department'),
        'filter_params': {
            'budget': request.GET.get('budget', ''),
            'date_from': request.GET.get('date_from', ''),
            'date_to': request.GET.get('date_to', ''),
        }
    }
    
    return render(request, 'comptabilite/list.html', context)