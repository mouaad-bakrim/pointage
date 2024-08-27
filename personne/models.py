from django.db import models

# Create your models here.
# Create your models here.
# dans votre application principale (par exemple, `myapp/models.py`)
from  Departement.models import Departement # Importez le modèle Departement
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from Departement.models import Departement

class User(AbstractUser):
    statut = models.CharField(max_length=50, default='Admine')
    idp = models.OneToOneField('personne.Pointeur', on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    
    def clean(self):
        super().clean()
        if self.statut == 'Admine' and self.idp is not None:
            raise ValidationError('Le champ idp doit être NULL pour les utilisateurs de type Admine.')
        if self.statut != 'Admine' and self.idp is None:
            raise ValidationError('Le champ idp ne peut pas être NULL pour les utilisateurs de type Pointeur.')
    
    def __str__(self):
        return f"{self.username} ({self.statut})"
    class Meta:
        db_table = 'User'
class Pointeur(models.Model):
    idP = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    date_de_naissance = models.DateField()
    date_d_embauche = models.DateField()
    cni = models.CharField(max_length=20, unique=True)
    cnss = models.CharField(max_length=20, unique=True)
    adresse = models.TextField()
    email = models.EmailField(max_length=254 )
    SEXE_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
    ]
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default='M')
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True)
    #groups = models.ManyToManyField(Group, related_name='pointeur_groups', blank=True)
    #user_permissions = models.ManyToManyField(Permission, related_name='pointeur_user_permissions', blank=True)
    class Meta:
        db_table = 'pointeur'

    def __str__(self):
        return f"{self.nom} {self.prenom}"
class Employe(models.Model):
    idE = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    date_de_naissance = models.DateField()
    date_d_embauche = models.DateField()
    cni = models.CharField(max_length=20, unique=True)
    cnss = models.CharField(max_length=20, unique=True)
    adresse = models.TextField()
    qualification = models.CharField(max_length=100)
    SEXE_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
    ]
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default='M')
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.nom} {self.prenom}"
