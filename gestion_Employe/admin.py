from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CV, Pointage ,Conge , ListeStatut , Point_PDF

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('ID_cv', 'nom_prenom', 'document', 'departement')
    search_fields = ('nom_prenom',)
    list_filter = ('departement',)
    ordering = ('nom_prenom',)

@admin.register(Pointage)
class PointageAdmin(admin.ModelAdmin):
    list_display = ('idP', 'jour', 'statut', 'departement', 'employe')
    #search_fields = ('employe__nom_prenom', 'departement__nom')
    list_filter = ('statut', 'departement', 'employe')
    ordering = ('jour', 'employe')
@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ('Idc', 'employe', 'date_debut', 'date_fin', 'document')
    #search_fields = ('employe__nom_prenom',)  # Permet de rechercher par le nom complet de l'employé
    list_filter = ('date_debut', 'date_fin', 'employe')  # Filtrage par date de début, fin et employé
    ordering = ('date_debut', 'employe')  # Tri par date de début et employé

admin.site.register(ListeStatut)
admin.site.register(Point_PDF)