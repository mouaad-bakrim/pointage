from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Pointeur,Employe
from  Departement.models import Departement
from  gestion_Employe.models import CV, Pointage , Conge , ListeStatut , Point_PDF
# Create your views here.
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import json
from django.conf import settings
from django.utils.crypto import get_random_string
from Departement.models import Departement
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password
import random
import string
from django.core.exceptions import ValidationError
from personne.models import Pointeur, User, Departement 
from django.contrib.auth import logout
from django.db.models import Q
from datetime import datetime, timedelta
import calendar
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from io import BytesIO
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def add_default_statuts():
    statuts = ['Absent', 'Congé', 'Présent']
    for nom in statuts:
        if not ListeStatut.objects.filter(nom=nom).exists():
            ListeStatut.objects.create(nom=nom)

@csrf_protect
def page_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user using Django's authentication system
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if the user is an Admine or Pointeur
            if user.statut == 'Admine':
                auth_login(request, user)
                return redirect('HelloAdmine')
            elif user.statut == 'Pointeur':
                auth_login(request, user)
                #return HttpResponse("Vous êtes connecté en tant que Pointeur.")
                return redirect('HelloPointeur')
        else:
            # Invalid credentials
            return render(request, 'personne/page_login.html', {'error': 'Identifiants invalides.'})
    
    return render(request, 'personne/page_login.html')
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def oblie_mot_pass(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        User = get_user_model()

        try:
            user = User.objects.filter(email=username).first()
            # Générer un nouveau mot de passe aléatoire
            new_password = generate_random_password()

            # Hacher le mot de passe
            hashed_password = make_password(new_password)
            user.set_password(new_password)
            user.save()

            # Envoyer le nouveau mot de passe par e-mail
            subject = 'Nouveau mot de passe'
            message = f'Bonjour {username} ,\nvoici votre nouveau mot de passe : {new_password}'
            from_email = 'votre_adresse_email@gmail.com'
            recipient_list = [user.email]

            # Envoyer l'e-mail avec le nouveau mot de passe
            send_mail(subject, message, from_email, recipient_list)
            
            return render(request, 'personne/page_login.html', {'bien_rec': 'bien_recu'})
        
        except User.DoesNotExist:
            return render(request, 'personne/oblie_mot_pass.html', {'error': 'Nom d’utilisateur non trouvé.'})
    
    return render(request, 'personne/oblie_mot_pass.html')

@login_required
def HelloAdmine(request):
    if request.user.statut != 'Admine':
        return redirect('page_login')                                                                                    
    add_default_statuts()
    today = timezone.now().date()

    # Calculer les statistiques
    user_count = Employe.objects.count()  # Nombre d'employés
    voy_count = Departement.objects.count()  # Nombre de départements
     # Nombre de congés

    # Récupérer les statuts
    absent_statut = ListeStatut.objects.get(nom='Absent')
    conge_statut = ListeStatut.objects.get(nom='Congé')
    present_statut = ListeStatut.objects.get(nom='Présent')

    absent_count = Pointage.objects.filter(jour=today, statut=absent_statut).count()  # Nombre de personnes absentes aujourd'hui
    comd_count = Pointage.objects.filter(jour=today, statut=conge_statut).count()
    departements = Departement.objects.all()

    data = []
    for departement in departements:
        pointeurs = Pointeur.objects.filter(departement=departement)
        pointages = Pointage.objects.filter(departement=departement, jour=today)

        presence_count = pointages.filter(statut=present_statut).count()
        absence_count = pointages.filter(statut=absent_statut).count()
        conge_count = pointages.filter(statut=conge_statut).count()

        if presence_count > 0 or absence_count > 0:
            data.append({
                'departement': departement,
                'pointeurs': pointeurs,
                'presence_count': presence_count,
                'absence_count': absence_count,
                'conge_count': conge_count,
            })

    start_date = today.replace(day=1)
    end_date = today.replace(day=calendar.monthrange(today.year, today.month)[1])

    # Génère toutes les dates du mois en cours
    dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    absences_data = [
    {
        'date': date.strftime('%d/%m'), 
        'count': Pointage.objects.filter(jour=date, statut=absent_statut).count() if date <= today else 0
    }
    for date in dates
    ]

    conges_data = [
    {
        'date': date.strftime('%d/%m'), 
        'count': Pointage.objects.filter(jour=date, statut=conge_statut).count() if date <= today else 0
    }
    for date in dates
    ]
    
    context = {
        'user_count': user_count,
        'voy_count': voy_count,
        'comd_count': comd_count,
        'absent_count': absent_count,
        'date_dujour': today,
        'data': data,
        'absences_data': json.dumps(absences_data),  # Convertir en JSON
        'conges_data': json.dumps(conges_data),
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'personne/HelloAdmine.html', context)
from personne.models import User

@login_required
def Pointeurs(request):
    if request.user.statut != 'Admine':
        return redirect('page_login')

    # Récupérer le terme de recherche
    search_query = request.GET.get('search', '')

    # Récupérer le nombre d'éléments à afficher
    number = request.GET.get('number', '50')

    # Filtrer les pointeurs par nom ou prénom si un terme de recherche est fourni
    pointeurs = Pointeur.objects.all()
    if search_query:
        pointeurs = pointeurs.filter(nom__icontains=search_query) | pointeurs.filter(prenom__icontains=search_query)
    
    pointeurs = pointeurs.order_by('nom')
    # Pagination
    paginator = Paginator(pointeurs, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'personne/Pointeurs.html', {
        'pointeurs': page_obj,
        'search_query': search_query,
        'number': number
    })

@login_required
def AjoutPointeur(request):
    if request.user.statut != 'Admine':
        return redirect('page_login')
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        date_de_naissance = request.POST.get('date_de_naissance')
        date_d_embauche = request.POST.get('date_d_embauche')
        cni = request.POST.get('cni')
        cnss = request.POST.get('cnss')
        adresse = request.POST.get('adresse')
        sexe = request.POST.get('sexe')
        departement_id = request.POST.get('departement')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Vérifier si des champs sont manquants
        if not all([nom, prenom, email, telephone, date_de_naissance, date_d_embauche, cni, cnss, adresse, sexe, departement_id, password, confirm_password]):
            return render(request, 'personne/AjoutPointeur.html', {'departments': Departement.objects.all(), 'error': 'Tous les champs sont requis.'})

        # Vérifier que les mots de passe correspondent
        if password != confirm_password:
            return render(request, 'personne/AjoutPointeur.html', {'departments': Departement.objects.all(), 'error': 'Les mots de passe ne correspondent pas.'})

        try:
            departement_id = int(departement_id)
            departement = Departement.objects.get(id_Dep=departement_id)
        except (ValueError, Departement.DoesNotExist):
            return render(request, 'personne/AjoutPointeur.html', {'departments': Departement.objects.all(), 'error': 'Département invalide.'})

        # Créer un pointeur
        pointeur = Pointeur.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            date_de_naissance=date_de_naissance,
            date_d_embauche=date_d_embauche,
            cni=cni,
            cnss=cnss,
            adresse=adresse,
            sexe=sexe,
            departement=departement
        )
        employe = Employe.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            date_de_naissance=date_de_naissance,
            date_d_embauche=date_d_embauche,
            cni=cni,
            cnss=cnss,
            adresse=adresse,
            sexe=sexe,
            departement=departement,
            qualification='Pointeur'
        )

        # Créer un utilisateur associé au pointeur
        username = f"{nom}_{prenom}"
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            statut='Pointeur',
            idp=pointeur
        )

        # Envoyer un e-mail à l'utilisateur avec ses informations de connexion
        subject = 'Votre compte Pointeur'
        salutation = f"Mr. {nom} {prenom}" if sexe == 'M' else f"Ms. {nom} {prenom}"
        message = (
            f"{salutation},\n\n"
            "Vous avez un compte Pointeur dans notre application.\n\n"
            f"Département: {departement.nom}\n\n"
            f"Authentification:\n"
            f"Username: {username}\n"
            f"Mot de passe: {password}\n\n"
            "Merci."
        )

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return redirect('Pointeurs')
    else:
        departments = Departement.objects.all()

    return render(request, 'personne/AjoutPointeur.html', {'departments': departments})

from django.core.paginator import Paginator

@login_required
def Departements(request):
    if request.user.statut != 'Admine':
        return redirect('page_login')

    # Récupérer le terme de recherche
    search_query = request.GET.get('search', '')

    # Récupérer le nombre d'éléments à afficher
    number = request.GET.get('number', '50')

    # Filtrer les départements par nom si un terme de recherche est fourni
    departements = Departement.objects.all()
    if search_query:
        departements = departements.filter(nom__icontains=search_query)
    #pointeurs = pointeurs.order_by('nom')
    departements = departements.order_by('nom')
    # Pagination
    paginator = Paginator(departements, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Departement/Departements.html', {
        'departements': page_obj,
        'search_query': search_query,
        'number': number
    })
@login_required
def AjoutDepartement(request):
    if request.user.statut != 'Admine':
     return redirect('page_login')
    if request.method == 'POST':
        # Retrieve form data from POST request
        nom = request.POST.get('nom')
        site = request.POST.get('site')
        adresse = request.POST.get('adresse')
        numero_telephone = request.POST.get('numero_telephone')

        # Create and save new Departement instance
        if nom and site and adresse and numero_telephone:
            Departement.objects.create(
                nom=nom,
                site=site,
                adresse=adresse,
                numero_telephone=numero_telephone
            )
            return redirect('Departements')  # Redirect to the department list page after saving

    return render(request, 'Departement/AjoutDepartement.html')

@login_required
def CVS(request):
    if request.user.statut != 'Admine':
        return redirect('page_login')

    # Récupérer le terme de recherche
    search_query = request.GET.get('search', '')

    # Récupérer le nombre d'éléments à afficher
    number = request.GET.get('number', '50')

    # Filtrer les CVs par nom_prenom si un terme de recherche est fourni
    cvs = CV.objects.all()
    if search_query:
        cvs = cvs.filter(
        Q(nom_prenom__icontains=search_query) |
        Q(niveau_etude__icontains=search_query)  # Ajouter cette ligne pour filtrer par niveau d'étude
    )
    # Trier les CVs par nom_prenom
    cvs = cvs.order_by('nom_prenom')

    # Pagination
    paginator = Paginator(cvs, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gestion_Employe/CVS.html', {
        'cvs': page_obj,
        'search_query': search_query,
        'number': number
    })

@login_required
def espace_personnelle(request):
    if request.user.statut != 'Admine':
     return redirect('page_login')
    return render(request, 'personne/Espace_personnelle_ad.html')

@login_required
def modifier_mot_de_passe(request):
    if request.user.statut != 'Admine':
     return redirect('page_login')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'personne/Espace_personnelle_ad.html', {
                'error': 'Les mots de passe ne correspondent pas.'
            })

        if not request.user.check_password(old_password):
            return render(request, 'personne/Espace_personnelle_ad.html', {
                'error': 'Le mot de passe actuel est incorrect.'
            })

        user = request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return render(request, 'personne/Espace_personnelle_ad.html', {
            'bien_rec': True
        })
    
    return render(request, 'personne/Espace_personnelle_ad.html')

@login_required
def Conges(request):
    if request.user.statut != 'Admine':
        return redirect('page_login')

    # Récupérer le terme de recherche
    search_query = request.GET.get('search', '')

    # Récupérer le nombre d'éléments à afficher
    number = request.GET.get('number', '50')

    # Filtrer les congés par nom ou prénom de l'employé si un terme de recherche est fourni
    conges = Conge.objects.all()
    if search_query:
        conges = conges.filter(
            Q(employe__nom__icontains=search_query) |
            Q(employe__prenom__icontains=search_query) |
            Q(reference__icontains=search_query)
        )

    # Trier les congés par nom d'employé et date de début
    conges = conges.order_by('employe__nom', 'date_debut')

    # Pagination
    paginator = Paginator(conges, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gestion_Employe/Conges.html', {
        'conges': page_obj,
        'search_query': search_query,
        'number': number
    })

from reportlab.lib.colors import grey
def generate_pdf(request, conge_id):
    # Retrieve the Conge object
    conge = get_object_or_404(Conge, pk=conge_id)

    # Create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    # Styles
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    
    # Add the three lines at the top-left corner
    line_style = ParagraphStyle(name='LineStyle', fontSize=12, alignment=0, spaceAfter=10)
    story.append(Paragraph('.....................', line_style))
    story.append(Paragraph('.....................', line_style))
    story.append(Paragraph('.................', line_style))
    story.append(Spacer(1, 30))  # Increased space between lines and "Agadir le"

    # Adjust the position of the date and the title
    header_style = ParagraphStyle(name='Header', fontSize=12, alignment=2, spaceAfter=20)
    header = Paragraph(f'Agadir le : {conge.date_demande.strftime("%d/%m/%Y")}', header_style)
    story.append(header)
    story.append(Spacer(1, 30))  # Increased space between "Agadir le" and the title

    # Title with border and background color
    title_style = ParagraphStyle(name='Title', fontSize=17, alignment=1, spaceAfter=30,
                                 textColor='black', backgroundColor=grey)
    # Add border and padding manually using Table
    
    
    title_table = Table([[Paragraph('<b>DECISION DE CONGE</b>', title_style)]],
                        colWidths=[250],  # Adjust width as needed, reduced width
                        style=[('BACKGROUND', (0, 0), (-1, -1), grey),
                               ('TEXTCOLOR', (0, 0), (-1, -1), 'black'),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('BOX', (0, 0), (-1, -1), 0.5, 'black'),  # Reduced border width
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 20),  # Increased padding at the bottom
                               ('TOPPADDING', (0, 0), (-1, -1), 10),
                               ('LEFTPADDING', (0, 0), (-1, -1), 10),
                               ('RIGHTPADDING', (0, 0), (-1, -1), 10)])
    story.append(title_table)
    story.append(Spacer(1,40))   # Increased space between the title and the content

    # Content
    content_style = ParagraphStyle(name='Content', fontSize=17, spaceAfter=20, alignment=0)
    content = [
        Paragraph(f'Reférence : <strong>{conge.reference}</strong>', content_style),
        Paragraph(f'Mr/Mme <strong>{conge.employe.nom} {conge.employe.prenom}</strong>.', content_style),
        Paragraph(f'CIN n° <strong>{conge.employe.cni}</strong> Immatriculé CNSS n° <strong>{conge.employe.cnss}</strong>.', content_style),
        Paragraph(f'Est autorisé(e) à sortir en congé par sa demande pendant la', content_style),
        Paragraph(f'période allant du <strong>{conge.date_debut.strftime("%d/%m/%Y")}</strong> au <strong>{conge.date_fin.strftime("%d/%m/%Y")}</strong> inclus.', content_style),
        Paragraph(f'Le nombre de jours de congé sera déduit du congé annuel', content_style),
        Paragraph(f'non soldé.', content_style),
    ]
    story.extend(content)
    story.append(Spacer(1, 40))  # Increased space between content and signature section

    # Signature
    signature_style = ParagraphStyle(name='Signature', fontSize=17, alignment=1, spaceAfter=30)
    signature = Table([
        [Paragraph('L\'administration', signature_style), Paragraph('L\'intéressé(e)', signature_style)],
        [Paragraph('..............................', signature_style), Paragraph('..............................', signature_style)]
    ], colWidths=[250, 250])
    signature.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('LEFTPADDING', (0, 1), (-1, 1), 10),
        ('RIGHTPADDING', (0, 1), (-1, 1), 10),
    ]))
    story.append(signature)

    # Build PDF
    doc.build(story)

    # Move the cursor to the beginning of the buffer
    buffer.seek(0)

    # Create the HTTP response with the PDF data
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="conge_{conge_id}.pdf"'
    return response

def deconnexion(request):
    logout(request)
    return redirect('page_login')

@login_required
def Pointages(request):
    # Vérifier si l'utilisateur est un administrateur
    if request.user.statut != 'Admine':
        return redirect('page_login')

    # Récupérer le nom du département (obligatoire) et la date (optionnelle)
    search_query = request.GET.get('search', '')
    date_query = request.GET.get('date', '')

    # Récupérer le nombre d'éléments à afficher
    number = request.GET.get('number', '50')

    # Filtrer les pointages par nom du département et par date si fournie
    pointages = Point_PDF.objects.all()

    if search_query:
        pointages = pointages.filter(departement__nom__icontains=search_query)

    if date_query:
        pointages = pointages.filter(jour=date_query)

    # Trier les pointages par nom du département et date
    pointages = pointages.order_by('departement__nom', 'jour')

    # Pagination
    paginator = Paginator(pointages, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gestion_Employe/pointages.html', {
        'pointages': page_obj,
        'search_query': search_query,
        'date_query': date_query,
        'number': number
    })