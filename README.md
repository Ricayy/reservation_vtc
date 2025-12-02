# reservation_vtc
A faire :
- Enregister saisie dans formulaire sur la bdd
- Map
- Auto complétion sur saisie adresse
- Liste déroulante pour véhicule
- Saisie par défaut
- Authentification
- Multilangues
- Style
- Notification des courses par mail, sms ou autres
- Interface de suivi des réservations
- Pages informations, avis, services, ...
- Header et footer

# Commandes Django
Création d'un projet Django
django-admin startproject <nom du projet>

Création App
python manage.py startapp <nom de l'app>

Actualisation du fichier settings.py (au moment de l'ajout d'une nouvelle App)
python manage.py migrate

Création model dans database
python manage.py makemigrations <nom de l'app>

Affiche la ligne selectionné depuis la database
python manage.py sqlmigrate <nom de l'app> <id de la ligne> 

Lancer le serveur
python manage.py runserver


