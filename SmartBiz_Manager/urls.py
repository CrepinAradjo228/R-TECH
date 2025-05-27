
from django.urls import path, include
from SmartBiz_Manager import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('gestion_ventes/',views.ventes,name='ventes'),
]