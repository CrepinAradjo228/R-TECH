from django.urls import path, include
from SmartBiz_Manager import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Chemin pour la gestion des ventes - panier
    path('ventes/', views.index, name='ventes'),  # j'ai changé '' en 'vente/' pour éviter conflit avec home
    # path('ventes/panier/', views.afficher_panier, name='afficher_panier'),
    # path('ventes/panier/ajouter/<int:article_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    # path('ventes/panier/modifier/<int:article_id>/', views.modifier_quantite_panier, name='modifier_quantite_panier'),
    # path('ventes/panier/supprimer/<int:article_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    # path('ventes/panier/valider/', views.valider_vente, name='valider_vente'),
    path('panier/', views.afficher_panier, name='afficher_panier'),
    path('panier/ajouter/<int:article_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/supprimer/<int:article_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('panier/vider/', views.vider_panier, name='vider_panier'),
    path('panier/modifier/<int:article_id>/', views.modifier_quantite, name='modifier_quantite'),
    path('panier/valider/', views.valider_vente, name='valider_vente'),
    path('vente/<int:vente_id>/', views.detail_vente, name='detail_vente'),
    path('supprimer_vente/<int:vente_id>/', views.supprimer_vente, name='supprimer_vente'),

        



    path('articles/', views.articles, name='articles'),
    path('ajout_article/', views.ajout_article, name='ajout_article'),

    # Chemin pour les analyses
    path('analyse/', views.analyse, name='analyse'),


    path('articles/modifier/<int:pk>/', views.modifier_article, name='modifier_article'),
    path('articles/supprimer/<int:pk>/', views.supprimer_article, name='supprimer_article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


