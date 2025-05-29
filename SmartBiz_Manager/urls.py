
from django.urls import path, include
from SmartBiz_Manager import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('gestion_ventes/',views.ventes,name='ventes'),

    

    path('gestion_ventes/', views.ventes, name='ventes'),
    path('articles/', views.articles, name='articles'),
    path('ajout_article/', views.ajout_article, name='ajout_article')

]