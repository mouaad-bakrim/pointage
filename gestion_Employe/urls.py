from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
path('HelloPointeur/', views.HelloPointeur, name='HelloPointeur'),
path('Employes/', views.Employes, name='Employes'),
path('AjoutEmploye/',views.AjoutEmploye, name='AjoutEmploye'),
path('CVS_Dep/',views.CVS_Dep, name='CVS_Dep'),
path('AjouterCV/', views.AjouterCV, name='AjouterCV'),
#path('Espace_Personelle/',views.Espace_Perso_Po, name='Espace_Perso_Po'),
#path('Modifier_Mot_passe/',views.Modifier_Mot_passe, name='Modifier_Mot_passe'),
path('Espace_Pers/', views.modifier_mot_de_passe1, name='modifier_mot_de_passe_po'),
path('Conges_Dep/', views.Conges_Dep, name='Conges_Dep'),
path('AjoutConge/', views.AjoutConge, name='AjoutConge'),
path('Pointage_Dep/',views.Pointage_Dep, name='Pointage_Dep'),
path('AjoutPointage/', views.AjoutPointage, name='AjoutPointage'),
path('traitement_pointage/', views.traitement_pointage, name='traitement_pointage'),
    # Ajoutez d'autres URL selon vos besoins
]