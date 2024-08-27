from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
 path('', views.page_login, name='page_login'),
 path('Mot_de_passe_oublie/', views.oblie_mot_pass, name='oblie_mot_pass'),
 path('HelloAdmine/', views.HelloAdmine, name='HelloAdmine'),
 path('Pointeurs/', views.Pointeurs, name='Pointeurs'),
 path('AjoutPointeur/', views.AjoutPointeur, name='AjoutPointeur'),
 path('Departements/', views.Departements, name='Departements'),
 path('AjoutDepartement/', views.AjoutDepartement, name='AjoutDepartement'),
 path('CVS/', views.CVS, name='CVS'),
 path('Pointages/', views.Pointages, name='Pointages'),
 path('Conges/', views.Conges, name='Conges'),
 path('Espace_Personnelle/', views.espace_personnelle, name='Espace_Personnelle'),
path('modifier_mot_de_passe/', views.modifier_mot_de_passe, name='modifier_mot_de_passe'),
path('deconnexion/', views.deconnexion, name='deconnexion'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)