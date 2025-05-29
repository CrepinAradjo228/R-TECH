from django.urls import path, include
from SmartBiz_Manager import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('gestion_ventes/',views.ventes,name='ventes'),
    

    

    path('gestion_ventes/', views.ventes, name='ventes'),
    path('articles/', views.articles, name='articles'),
    path('ajout_article/', views.ajout_article, name='ajout_article'),

        #chemin pour les analyses
    path('analyse/', views.analyse, name='analyse'),

    path('articles/modifier/<int:pk>/', views.modifier_article, name='modifier_article'),
    path('articles/supprimer/<int:pk>/', views.supprimer_article, name='supprimer_article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)