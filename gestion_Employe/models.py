from django.db import models

# Create your models here.
from django.db import models
from  Departement.models import Departement
from  personne.models import Employe
from datetime import date
from django.utils import timezone
# Create your models here.
class CV(models.Model):
    ID_cv = models.AutoField(primary_key=True)
    nom_prenom = models.CharField(max_length=255)
    date_naissance = models.DateField(null=True, blank=True)
    situation_familiale = models.CharField(max_length=100)  # Stockée sous forme de texte
    adresse = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    telephone = models.CharField(max_length=20)
    niveau_etude = models.CharField(max_length=255)
    diplomes = models.TextField(null=True, blank=True)
    experiences = models.TextField(null=True, blank=True)
    permis_de_conduites = models.JSONField(default=dict)
    langages = models.TextField(null=True, blank=True)
    infos_complementaires = models.TextField(null=True, blank=True)
    document = models.FileField(upload_to='cv_documents/')
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    date_depot = models.DateField(default=date.today)
    def __str__(self):
        return f'{self.nom_prenom} - {self.ID_cv}'
  
class ListeStatut(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom 
    
class Pointage(models.Model):
    idP = models.AutoField(primary_key=True)
    jour = models.DateField()  # Utilisez DateTimeField si vous avez besoin d'une date et heure
    statut = models.ForeignKey(ListeStatut, on_delete=models.CASCADE)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.employe.nom} - {self.jour} '
    
class Conge(models.Model):
    Idc = models.AutoField(primary_key=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)  # Lien vers le modèle Employe
    date_debut = models.DateField()  # Date de début du congé
    date_fin = models.DateField()  # Date de fin du congé
    date_demande = models.DateField(default=timezone.now)  # Date de la demande de congé
    reference = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Autoriser temporairement les valeurs nulles  # Référence unique pour le congé

    def __str__(self):
        return f'{self.employe} - {self.date_debut} au {self.date_fin}'
    
class Point_PDF(models.Model):
    idPD = models.AutoField(primary_key=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    jour = models.DateField()
    P_PDF = models.FileField(upload_to='pdf_pointage/')

    def __str__(self):
        return f'PDF for {self.departement.nom} on {self.jour}'

