from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from personne.models import Pointeur, Employe
from .models import  Pointage ,CV ,Conge , ListeStatut
import json
from Departement.models import Departement
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Point_PDF
from datetime import date
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from .models import Employe, ListeStatut, Pointage, Departement, Point_PDF
from datetime import date
from django.conf import settings
from datetime import datetime, timedelta, date
import calendar
import uuid
from django.shortcuts import get_object_or_404
# Create your views here.
def add_default_statuts():
    statuts = ['Absent', 'Congé', 'Présent']
    for nom in statuts:
        if not ListeStatut.objects.filter(nom=nom).exists():
            ListeStatut.objects.create(nom=nom)

@login_required
def HelloPointeur(request):
    user = request.user
    
    # Vérifiez si l'utilisateur est un Pointeur
    if user.statut != 'Pointeur':
        return redirect('page_login')  # Rediriger vers la page de connexion ou une page d'erreur
    add_default_statuts()
    # Accéder à l'objet Pointeur associé à l'utilisateur
    pointeur = user.idp
    
    # Vérifier si le pointeur est associé à un département
    if not pointeur or not pointeur.departement:
        # Gérer le cas où le pointeur ou son département est manquant
        return redirect('page_login')  # Rediriger vers la page de connexion ou une page d'erreur

    department = pointeur.departement
    today = timezone.now().date()

    # Récupérer les statuts
    absent_statut = ListeStatut.objects.get(nom='Absent')
    conge_statut = ListeStatut.objects.get(nom='Congé')

    # Calcul des statistiques pour le département du Pointeur
    # Obtenez le premier et le dernier jour du mois en cours
    start_date = today.replace(day=1)
    end_date = today.replace(day=calendar.monthrange(today.year, today.month)[1])

    # Générez les données d'absence pour tout le mois
    absences_data = [
    {'date': (start_date + timedelta(days=i)).strftime('%d/%m'),
     'count': Pointage.objects.filter(jour=start_date + timedelta(days=i), statut=absent_statut, departement=department).count()}
    for i in range((end_date - start_date).days + 1)
    ]

    # Générez les données de congés pour tout le mois
    conges_data = [
    {'date': (start_date + timedelta(days=i)).strftime('%d/%m'),
     'count': Pointage.objects.filter(jour=start_date + timedelta(days=i), statut=conge_statut, departement=department).count()}
    for i in range((end_date - start_date).days + 1)
    ]

    # Calcul des nouvelles statistiques
    emp_count = Employe.objects.filter(departement=department).count()
    #cv_count = CV.objects.filter(departement=department).count()
    cv_count =Pointage.objects.filter(jour=today, statut=conge_statut, departement=department).count()
    absent_count_today = Pointage.objects.filter(jour=today, statut=absent_statut, departement=department).count()

    context = {
        'user': user,
        'pointeur': pointeur,
        'departement': department,
        'absences_data': json.dumps(absences_data),
        'conges_data': json.dumps(conges_data),
        'start_date': start_date,
        'end_date': end_date,
        'Emp_count': emp_count,
        'Dep_Nom': department.nom,
        'Dep_site': department.site,
        'CV_count': cv_count,
        'absent_count': absent_count_today
    }
    return render(request, 'Pointeur/HelloPointeur.html', context)
@login_required
def Employes(request):
    user = request.user

    # Vérifiez si l'utilisateur est un Pointeur, sinon redirigez vers la page de connexion
    if user.statut != 'Pointeur':
        return redirect('page_login')

    # Accédez à l'objet Pointeur associé à l'utilisateur
    pointeur = user.idp

    # Vérifiez si le pointeur est associé à un département
    if not pointeur or not pointeur.departement:
        return redirect('page_login')

    department = pointeur.departement

    # Récupérer le terme de recherche
    search_query = request.GET.get('search', '')

    # Récupérer le nombre d'éléments à afficher
    number = request.GET.get('number', '50')

    # Filtrer les employés par le département du pointeur connecté et appliquer la recherche
    employees = Employe.objects.filter(departement=department)
    if search_query:
        employees = employees.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) 
        )

    # Trier les employés par nom
    employees = employees.order_by('nom')

    # Pagination
    paginator = Paginator(employees, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'employees': page_obj,
        'department': department,
        'search_query': search_query,
        'number': number,
    }
    return render(request, 'Pointeur/Employes.html', context)

@login_required
def AjoutEmploye(request):
    context = {}

    if request.user.is_authenticated:
        user = request.user

        if user.statut == 'Pointeur':
            if request.method == 'POST':
                nom = request.POST.get('nom')
                prenom = request.POST.get('prenom')
                email = request.POST.get('email')
                telephone = request.POST.get('telephone')
                date_naissance_str = request.POST.get('date_de_naissance')  # Valeur de date de naissance
                date_embauche_str = request.POST.get('date_d_embauche')    # Valeur de date d'embauche
                cni = request.POST.get('cni')
                cnss = request.POST.get('cnss')
                adresse = request.POST.get('adresse')
                sexe = request.POST.get('sexe')
                qualification = request.POST.get('qualification')

                # Convertir les chaînes de caractères en objets date si elles ne sont pas vides
                from datetime import datetime

                try:
                    date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d').date() if date_naissance_str else None
                    date_embauche = datetime.strptime(date_embauche_str, '%Y-%m-%d').date() if date_embauche_str else None
                except ValueError:
                    date_naissance = None
                    date_embauche = None

                # Assurez-vous que le pointeur a un département associé
                departement = user.idp.departement
                departement_id = departement.id_Dep if departement else None

                # Créer l'employé en utilisant les données du formulaire et l'id du département du pointeur
                employe = Employe.objects.create(
                    nom=nom, prenom=prenom, email=email,
                    telephone=telephone, date_de_naissance=date_naissance,
                    date_d_embauche=date_embauche, cni=cni, cnss=cnss,
                    adresse=adresse, qualification=qualification,
                    sexe=sexe, departement_id=departement_id
                )

                # Rediriger vers une page de succès après l'ajout de l'employé
                return redirect('Employes')

            return render(request, 'Pointeur/AjoutEmploye.html', context)
        else:
            return redirect('page_login')  # Redirection vers la page de connexion si l'utilisateur n'est pas un Pointeur
    else:
        return redirect('page_login')


@login_required
def CVS_Dep(request):
    user = request.user

    # Vérifiez si l'utilisateur est un Pointeur
    if user.statut != 'Pointeur':
        return redirect('page_login')

    # Accédez à l'objet Pointeur associé à l'utilisateur
    pointeur = user.idp

    # Vérifiez si le pointeur est associé à un département
    if not pointeur or not pointeur.departement:
        return redirect('page_login')

    department = pointeur.departement

    # Récupérer le terme de recherche
    search_query = request.GET.get('search', '')

    # Récupérer le nombre d'éléments à afficher
    number = request.GET.get('number', '50')

    # Filtrer les CVs par le département du pointeur connecté et appliquer la recherche
    cvs = CV.objects.filter(departement=department)
    if search_query:
        cvs = cvs.filter(
        Q(nom_prenom__icontains=search_query) |
        Q(departement__nom__icontains=search_query) |
        Q(niveau_etude__icontains=search_query)  # Ajouter cette ligne pour filtrer par niveau d'étude
        )

    # Trier les CVs par nom et prénom
    cvs = cvs.order_by('nom_prenom')

    # Pagination
    paginator = Paginator(cvs, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cvs': page_obj,
        'department': department,
        'search_query': search_query,
        'number': number,
    }
    return render(request, 'Pointeur/CVS_Dep.html', context)
@login_required
def AjouterCV(request):
    if request.user.statut == 'Pointeur':
        if request.method == 'POST':
            # Récupérer les données du formulaire
            nom_prenom = request.POST.get('nom_prenom')
            date_naissance = request.POST.get('date_naissance')
            situation_familiale = request.POST.get('situation_familiale')
            email = request.POST.get('email')
            telephone = request.POST.get('telephone')
            niveau_etude = request.POST.get('niveau_etude')
            diplomes = request.POST.get('diplomes')
            experiences = request.POST.get('experiences')
            permis_de_conduires = request.POST.getlist('permis_de_conduire')  # Liste de valeurs des permis
            langages = request.POST.get('langages')
            infos_complementaires = request.POST.get('infos_complementaires')
            document = request.FILES.get('document')

            # Récupérez le Pointeur et son département
            try:
                pointeur = request.user.idp
                departement = pointeur.departement

                if departement:
                    # Créez l'objet CV avec le département du pointeur
                    cv = CV.objects.create(
                        nom_prenom=nom_prenom,
                        date_naissance=date_naissance,
                        situation_familiale=situation_familiale,
                        email=email,
                        telephone=telephone,
                        niveau_etude=niveau_etude,
                        diplomes=diplomes,
                        experiences=experiences,
                        permis_de_conduites={'permis': permis_de_conduires},  # Stocker les permis sous forme de JSON
                        langages=langages,
                        infos_complementaires=infos_complementaires,
                        document=document,
                        departement=departement,
                        date_depot=date.today()
                    )
                    # Rediriger vers la liste des CVs
                    return redirect('CVS_Dep')
                else:
                    # Gérez le cas où le pointeur n'a pas de département associé
                    return render(request, 'Pointeur/AjoutCV.html', {'error': 'Aucun département associé.'})
            except Pointeur.DoesNotExist:
                # Gérez le cas où le Pointeur n'existe pas
                return render(request, 'Pointeur/AjoutCV.html', {'error': 'Pointeur introuvable.'})

        # Aucune donnée n'est postée, juste rendre le formulaire vide
        return render(request, 'Pointeur/AjoutCV.html')
    else:
        return redirect('page_login')


@login_required
def Espace_Perso_Po(request):
    user = request.user

    # Vérifiez si l'utilisateur est un Pointeur
    if user.statut != 'Pointeur':
        return redirect('page_login')
    pointeur = request.user.idp
    date_nais= pointeur.date_de_naissance.strftime('%Y-%m-%d')
    date_em=pointeur.date_d_embauche.strftime('%Y-%m-%d') # Exemple pour récupérer le pointeur connecté
    context = {
        'pointeur': pointeur,
        'date_de_naissanc': date_nais,
        'date_d_embauch':  date_em,
    }
    return render(request, 'Pointeur/Espace_Perso_Po.html', context)
@login_required
def Modifier_Mot_passe(request):
    user = request.user

    # Vérifiez si l'utilisateur est un Pointeur
    if user.statut != 'Pointeur':
        return redirect('page_login')
    return render(request, 'Pointeur/Modifier_Mot_passe.html')

@login_required
def modifier_mot_de_passe1(request):
    user = request.user

    # Vérifiez si l'utilisateur est un Pointeur
    if user.statut != 'Pointeur':
        return redirect('page_login')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'Pointeur/Modifier_Mot_passe.html', {
                'error': 'Les mots de passe ne correspondent pas.'
            })

        if not request.user.check_password(old_password):
            return render(request, 'Pointeur/Modifier_Mot_passe.html', {
                'error': 'Le mot de passe actuel est incorrect.'
            })

        user = request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return render(request, 'Pointeur/Modifier_Mot_passe.html', {
            'bien_rec': True
        })
    
    return render(request, 'Pointeur/Modifier_Mot_passe.html')

@login_required
def Conges_Dep(request):
    user = request.user

    # Vérifiez si l'utilisateur est un Pointeur
    if user.statut != 'Pointeur':
        return redirect('page_login')

    # Accédez à l'objet Pointeur associé à l'utilisateur
    pointeur = user.idp

    # Vérifiez si le pointeur est associé à un département
    if not pointeur or not pointeur.departement:
        return redirect('page_login')

    department = pointeur.departement

    # Récupérer le terme de recherche
    search_query = request.GET.get('search', '')

    # Récupérer le nombre d'éléments à afficher
    number = request.GET.get('number', '50')

    # Filtrer les Conges par le département du pointeur connecté et appliquer la recherche
    conges = Conge.objects.filter(employe__departement=department)
    if search_query:
        conges = conges.filter(
            Q(employe__nom__icontains=search_query) |
            Q(employe__prenom__icontains=search_query) 
        )

    # Trier les Conges par la date de début
    conges = conges.order_by('date_debut')

    # Pagination
    paginator = Paginator(conges, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'conges': page_obj,
        'department': department,
        'search_query': search_query,
        'number': number,
    }
    return render(request, 'Pointeur/Conges.html', context)

@login_required
def AjoutConge(request):
    if request.user.statut == 'Pointeur':
        # Obtenez le département de l'utilisateur connecté
        pointeur = request.user.idp
        departement = pointeur.departement
        employes = Employe.objects.filter(departement=departement)
        
        if request.method == 'POST':
            employe_id = request.POST.get('employe')
            date_debut = request.POST.get('date_debut')
            date_fin = request.POST.get('date_fin')

            if employe_id and date_debut and date_fin:
                try:
                    employe = Employe.objects.get(idE=employe_id)
                    # Créez un nouvel objet Congé avec une référence générée
                    conge = Conge(
                        employe=employe,
                        date_debut=date_debut,
                        date_fin=date_fin,
                        reference=f'RC{uuid.uuid4().hex[:6].upper()}'  # Génération de la référence
                    )
                    conge.save()
                    # Redirigez vers la page Conges
                    return redirect('Conges_Dep')
                except Employe.DoesNotExist:
                    # Gérez le cas où l'employé n'existe pas
                    return render(request, 'Pointeur/AjoutConge.html', {'employes': employes, 'error': 'Employé non trouvé'})
            else:
                # Gérez le cas où les champs requis sont vides
                return render(request, 'Pointeur/AjoutConge.html', {'employes': employes, 'error': 'Tous les champs doivent être remplis'})
        
        context = {
            'employes': employes,
        }
        return render(request, 'Pointeur/AjoutConge.html', context)
    else:
        return redirect('page_login')

@login_required
def Pointage_Dep(request):
    user = request.user

    # Verify if the user is a Pointeur
    if user.statut != 'Pointeur':
        return redirect('page_login')

    try:
        # Retrieve the Pointeur associated with the current user
        pointeur = Pointeur.objects.get(user=user)
        departement = pointeur.departement
    except Pointeur.DoesNotExist:
        return redirect('page_login')

    if not departement:
        return redirect('page_login')

    # Check if there are existing Pointages for today in the same department
    today = date.today()
    print(today)
    print(departement)
    existing_pointages_today = Pointage.objects.filter(
        departement=departement,
        jour=today
    ).exists()
    print(existing_pointages_today)
    # Retrieve the search date and the number of items to display
    search_date = request.GET.get('search_date', '')
    number = request.GET.get('number', '50')

    # Filter Pointages by the department of the logged-in Pointeur and apply the search
    pointages = Point_PDF.objects.filter(departement=departement)
    
    # Apply search filter by date
    if search_date:
        try:
            search_date = date.fromisoformat(search_date)  # Convert the string to a date object
            pointages = pointages.filter(jour=search_date)
        except ValueError:
            # Handle invalid date format
            pointages = pointages.none()  # or handle it as needed

    # Order Pointages by date
    pointages = pointages.order_by('jour')

    # Pagination
    paginator = Paginator(pointages, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'pointages': page_obj,
        'departement': departement,
        'search_date': search_date,
        'number': number,
        'display_button': not existing_pointages_today  # Add this condition
    }
    return render(request, 'Pointeur/Pointage_Dep.html', context)


@login_required
def AjoutPointage(request):
    user = request.user
    pointeur = Pointeur.objects.get(user=user)
    departement = pointeur.departement
    today = date.today()
    existing_pointages_today = Pointage.objects.filter(
        departement=departement,
        jour=today
    ).exists()
    if existing_pointages_today:
        return redirect('Pointage_Dep')
    # Vérifiez si l'utilisateur est un Pointeur
    if user.statut != 'Pointeur':
        return redirect('page_login')

    try:
        # Récupérer le Pointeur associé à l'utilisateur
        pointeur = Pointeur.objects.get(user=user)
        departement = pointeur.departement
    except Pointeur.DoesNotExist:
        return redirect('page_login')

    if not departement:
        return redirect('page_login')

    # Récupérer les employés du même département
    employes = Employe.objects.filter(departement=departement)

    # Récupérer les titres de colonnes depuis ListeStatut
    titres_statuts = ListeStatut.objects.all()

    context = {
        'employes': employes,
        'titres_statuts': titres_statuts,
        'today_date': date.today().strftime('%Y-%m-%d'),  # Passer la date actuelle au contexte
    }
    return render(request, 'Pointeur/AjoutPointage.html', context)

from django.utils.dateparse import parse_date
def traitement_pointage(request):
    if request.method == 'POST':
        jour_str = request.POST.get('jour')
        try:
            # Convertir la date au format YYYY-MM-DD
            jour = parse_date(jour_str)
            if not jour:
                raise ValueError("Invalid date format")

            # Récupérer les autres données du formulaire
            titres_statuts = ListeStatut.objects.all()
            employes = Employe.objects.all()
            print(f"Date reçue : {jour}")
            print(f"Employés : {employes}")
            print(f"Titre Statuts : {titres_statuts}")

            # Dictionnaire pour collecter les pointages pour le PDF
            pointages = []

            # Traiter chaque employé
            for employe in employes:
                statut_id = request.POST.get(f'employe_{employe.idE}')
                if statut_id:
                    try:
                        statut = ListeStatut.objects.get(id=statut_id)
                        print(f"Enregistrement : employe={employe}, statut={statut}, date={jour}")
                        pointage = Pointage.objects.create(
                            jour=jour,
                            statut=statut,
                            departement=employe.departement,
                            employe=employe
                        )
                        pointages.append({
                            'nom_prenom': f"{employe.nom} {employe.prenom}",
                            'qualification': employe.qualification,
                            'departement': employe.departement.nom + ' ' +employe.departement.site ,
                            'statut': statut.nom
                        })
                    except Exception as e:
                        print(f"Erreur lors de la création du pointage : {e}")

            # Générer le PDF
            if pointages:
                pdf_path = generer_pdf(departement=employe.departement, jour=jour, pointages=pointages)

                # Enregistrer le PDF dans la base de données
                Point_PDF.objects.create(
                    departement=employe.departement,
                    jour=jour,
                    P_PDF=pdf_path
                )

        except ValueError as e:
            # Gérer les erreurs de format de date ou autres erreurs
            print(f"Erreur de traitement de la date : {e}")
            return HttpResponse('Erreur de traitement')

        return redirect('Pointage_Dep')  # Remplacez par l'URL de succès appropriée

    return HttpResponse('ERREUR')


import os

def generer_pdf(departement, jour, pointages):
    # Chemin où enregistrer le PDF temporairement
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = TA_CENTER
    normal_style = styles['Normal']

    # Contenu du PDF
    elements = []

    # Titre du rapport
    title = Paragraph('Rapport de Presence', title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Espace

    # Date du jour
    date_paragraph = Paragraph(f'Date: {jour.strftime("%d/%m/%Y")}', normal_style)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 12))  # Espace

    # Données du tableau principal avec des colonnes élargies
    data = [['Nom et Prénom', 'Qualification', 'Département', 'Statut']]
    for pointage in pointages:
        data.append([pointage['nom_prenom'], pointage['qualification'], pointage['departement'], pointage['statut']])

    # Création du tableau principal avec colonnes élargies
    col_widths = [100, 100, 100, 100]  # Largeur de chaque colonne
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))  # Espace

    # Ajout de la statistique avec statut sur la première ligne
    stat_data = {}
    for pointage in pointages:
        stat_data[pointage['statut']] = stat_data.get(pointage['statut'], 0) + 1

    # Statut en première ligne
    stat_table_data = [['Statut'] + list(stat_data.keys())]
    stat_table_data.append(['Nombre'] + list(stat_data.values()))

    stat_table = Table(stat_table_data)
    stat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(Paragraph('Statistiques', styles['Heading2']))
    elements.append(stat_table)

    # Générer et sauvegarder le PDF
    doc.build(elements)
    buffer.seek(0)

    # Nom du fichier PDF
    pdf_filename = f"{departement.nom}_{jour.strftime('%Y%m%d')}.pdf"

    # Chemin de stockage du PDF
    media_root = settings.MEDIA_ROOT
    pdf_directory = os.path.join(media_root, 'pdf_pointage')
    pdf_path = os.path.join(pdf_directory, pdf_filename)

    # Créer le répertoire s'il n'existe pas
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    # Enregistrer le fichier
    with open(pdf_path, 'wb') as f:
        f.write(buffer.read())

    return pdf_path