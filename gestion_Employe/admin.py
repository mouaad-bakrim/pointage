from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CV, Pointage ,Conge , ListeStatut , Point_PDF

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('ID_cv', 'nom_prenom', 'departement', 'date_naissance', 'date_depot')
    search_fields = ('nom_prenom', 'email', 'departement__nom')
    list_filter = ('departement', 'date_depot', 'date_naissance')
    ordering = ('date_depot', 'nom_prenom')

@admin.register(Pointage)
class PointageAdmin(admin.ModelAdmin):
    list_display = ('idP', 'jour', 'statut', 'departement', 'employe')
    #search_fields = ('employe__nom_prenom', 'departement__nom')
    list_filter = ('statut', 'departement', 'employe')
    ordering = ('jour', 'employe')
@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ('Idc', 'employe', 'date_debut', 'date_fin', 'date_demande', 'reference')
    list_filter = ('date_debut', 'date_fin', 'employe', 'date_demande')  # Filtrage par date de demande également
    ordering = ('date_debut', 'employe')

admin.site.register(ListeStatut)
admin.site.register(Point_PDF)