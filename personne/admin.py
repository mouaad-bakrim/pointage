from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Pointeur, Employe ,User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class UserAdmin(BaseUserAdmin):
    #model = User
    list_display = ('username', 'statut', 'idp')
    search_fields = ('username', 'statut')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'statut', 'idp')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'statut', 'idp'),
        }),
    )

class PointeurAdmin(admin.ModelAdmin):
    list_display = ('idP', 'nom', 'prenom', 'departement')
    search_fields = ('nom', 'prenom')
    list_filter = ('departement',)
    ordering = ('nom',)

class EmployeAdmin(admin.ModelAdmin):
    list_display = ('idE', 'nom', 'prenom', 'email', 'departement')
    search_fields = ('nom', 'prenom', 'email')
    list_filter = ('departement',)
    ordering = ('nom',)
admin.site.register(Pointeur, PointeurAdmin)
admin.site.register(Employe, EmployeAdmin)
admin.site.register(User, UserAdmin)


