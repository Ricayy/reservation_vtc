# reservation_vtc
A faire :
- Suppression depuis formulaire sur la bdd
- Liste déroulante pour véhicule
- Saisie par défaut
- Map
- Auto complétion sur saisie adresse
- Authentification
- Multilangues
- Style
- Notification des courses par mail, sms ou autres
- Pages informations, avis, services, ...
- Header et footer
- Stripe
- Modèles Odoo Vehicule, Trajet, Contact
- Association Contact avec téléphone

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


