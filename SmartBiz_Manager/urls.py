from django.urls import path, include
from SmartBiz_Manager import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
        


    # Gestion des ventes (une seule fois)

    path('gestion_ventes/', views.ventes, name='ventes'),

    path('articles/', views.articles, name='articles'),
    path('ajout_article/', views.ajout_article, name='ajout_article'),

    # Chemin pour les analyses
    path('analyse/', views.analyse, name='analyse'),

    # Chemin pour la gestion des ventes - panier
    path('vente/', views.index, name='index'),  # j'ai changé '' en 'vente/' pour éviter conflit avec home
    path('vente/panier/', views.afficher_panier, name='afficher_panier'),
    path('vente/panier/ajouter/<int:article_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('vente/panier/modifier/<int:article_id>/', views.modifier_quantite_panier, name='modifier_quantite_panier'),
    path('vente/panier/supprimer/<int:article_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('vente/panier/valider/', views.valider_vente, name='valider_vente'),
]
