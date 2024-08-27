from django.db import models

# Create your models here.
from django.db import models
from  Departement.models import Departement
from  personne.models import Employe
# Create your models here.
class CV(models.Model):
    ID_cv = models.AutoField(primary_key=True)
    nom_prenom = models.CharField(max_length=255)
    document = models.FileField(upload_to='cv_documents/')
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)

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
    document = models.FileField(upload_to='conge_documents/')  # Champ pour le fichier PDF associé

    def __str__(self):
        return f'{self.date_debut} à {self.date_fin}'
    
class Point_PDF(models.Model):
    idPD = models.AutoField(primary_key=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    jour = models.DateField()
    P_PDF = models.FileField(upload_to='pdf_pointage/')

    def __str__(self):
        return f'PDF for {self.departement.nom} on {self.jour}'

