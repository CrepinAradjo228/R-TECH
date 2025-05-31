from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def _str_(self):
        return self.nom


class Article(models.Model):
    """
    Modèle pour les articles à afficher
    """
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_stock = models.IntegerField()
    categorie = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

# Create your models here.
class Vente(models.Model):
    articles = models.ManyToManyField(Article, related_name='ventes')
    nombreArticles = models.PositiveIntegerField()
    prixTotal = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)

    def _str_(self):
        return f"Vente {self.id} - {self.date}"
    
class LigneCommande(models.Model):
    vente = models.ForeignKey(Vente, related_name='lignes_commande', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_ligne(self):
        return self.quantite * self.prix_unitaire
    
    def __str__(self):
        return f"{self.quantite}x {self.article.nom} @ {self.prix_unitaire}€"
    
    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"


class Facture(models.Model):
    numeroFacture = models.CharField(max_length=50, unique=True)
    nomClient = models.CharField(max_length=100)
    telephoneClient = models.CharField(max_length=20)
    dateEmission = models.DateField()
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='factures')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    modePaiement = models.CharField(max_length=50)

    def _str_(self):
        return f"Facture {self.numeroFacture}"
