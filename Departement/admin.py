from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Departement

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('id_Dep', 'nom', 'adresse', 'numero_telephone')
    search_fields = ('nom', 'adresse')
    #list_filter = ('site',)
    ordering = ('nom',)
