from django.db import models

class Article(models.Model):
    """
    Modèle pour les articles à afficher
    """
    image = models.ImageField(upload_to='articles/')
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
