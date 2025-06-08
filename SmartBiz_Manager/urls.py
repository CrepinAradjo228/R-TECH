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
    path('ventes/facture/<int:vente_id>/', views.visualiser_facture, name='visualiser_facture'),
    path('ventes/facture/telecharger/<int:facture_id>/', views.export_facture_pdf, name='export_facture_pdf'),
    path('voir_cahier_comptable/', views.cahier_comptable, name='voir_cahier_comptable'),
    path('export-cahier-csv/', views.export_cahier_csv, name='export_cahier_csv'),
    
    #Gstion des budgets et departements 
    path('budget/create/', views.create_budget, name='create_budget'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budget/summary/', views.budget_summary, name='budget_summary'),
    path('department/create/', views.create_department, name='create_department'),
    path('departments/', views.department_list, name='department_list'),
    path('comptabilite/', views.comptabilite, name='comptabilite'),
    
    #Gestion des transactions 
    path('transactions/', views.transaction_list , name='transaction_list'),
    
    # path('transactions/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction_update'),
    # path('transactions/<int:pk>/delete/', TransactionDeleteView.as_view(), name='transaction_delete'),
       
    #Gestions des articles 


    path('articles/', views.articles, name='articles'),
    path('ajout_article/', views.ajout_article, name='ajout_article'),

    # Chemin pour les analyses
    path('analyse/', views.analyse, name='analyse'),


    path('articles/modifier/<int:pk>/', views.modifier_article, name='modifier_article'),
    path('articles/supprimer/<int:pk>/', views.supprimer_article, name='supprimer_article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


