from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Departement(models.Model):
    id_Dep = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    site = models.CharField(max_length=30)
    adresse = models.TextField()
    numero_telephone = models.CharField(max_length=15)
    #site = models.URLField(blank=True, null=True)  # Permet de laisser ce champ vide

    def __str__(self):
        return self.nom