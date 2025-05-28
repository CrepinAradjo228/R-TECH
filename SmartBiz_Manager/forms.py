from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['image', 'nom', 'description', 'prix_unitaire', 'quantite_stock', 'categorie']