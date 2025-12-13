# reservation_vtc
A faire :
- Affichage réservation depuis page profil pour user connecté
- Affichage réservation depuis page unique pour user invité
- Annulation réservation depuis page profil ou page unique
- Modèles Odoo Trajet
- Stripe
- Style
- Multilangues
- Notification des courses par mail, sms ou autres
- Pages informations, avis, services, ...
- Footer

# Commandes Django
Création d'un projet Django : 
django-admin startproject <nom du projet>

Création App : 
python manage.py startapp <nom de l'app>

Actualisation du fichier settings.py (au moment de l'ajout d'une nouvelle App) : 
python manage.py migrate

Création model dans database : 
python manage.py makemigrations <nom de l'app>

Affiche la ligne selectionné depuis la database : 
python manage.py sqlmigrate <nom de l'app> <id de la ligne> 

Lancer le serveur : 
python manage.py runserver


