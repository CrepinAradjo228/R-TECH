from django import forms
from .models import Article, Categorie, Budget, Transaction, Department

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['image', 'nom', 'description', 'prix_unitaire', 'quantite_stock', 'categorie']
        
        

#Gestion du budget et des trancsacs 


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['department', 'year', 'amount']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['budget', 'date', 'amount']
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nom du Département', 'class': 'form-control'}),
        }