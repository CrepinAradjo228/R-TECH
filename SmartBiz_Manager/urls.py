from django.urls import path, include
from SmartBiz_Manager import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Chemin pour la gestion des ventes - panier
    path('vente/', views.index, name='index'),  # j'ai changé '' en 'vente/' pour éviter conflit avec home
    path('vente/panier/', views.afficher_panier, name='afficher_panier'),
    path('vente/panier/ajouter/<int:article_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('vente/panier/modifier/<int:article_id>/', views.modifier_quantite_panier, name='modifier_quantite_panier'),
    path('vente/panier/supprimer/<int:article_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('vente/panier/valider/', views.valider_vente, name='valider_vente'),

        


    # Gestion des ventes (une seule fois)

    path('gestion_ventes/', views.ventes, name='ventes'),

    path('articles/', views.articles, name='articles'),
    path('ajout_article/', views.ajout_article, name='ajout_article'),

    # Chemin pour les analyses
    path('analyse/', views.analyse, name='analyse'),


    path('articles/modifier/<int:pk>/', views.modifier_article, name='modifier_article'),
    path('articles/supprimer/<int:pk>/', views.supprimer_article, name='supprimer_article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


