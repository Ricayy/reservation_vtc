# A faire :
- Style
- Notification des courses par email, sms ou autres
- Email de confirmation depuis serveur
- Annulation réservation depuis page profil ou page unique
- Affichage réservation depuis page unique pour user invité
- Pages informations, avis, services, ...
- Footer
- Ajout auto complete custom POI

# Fait :
- Formulaire de réservation (adresse, date, véhicule, info clients)
- Auto suggestions/complétions sur les champs d'adresses
- Prévisualisation du trajet et calcul de la distance et du prix en fonction du véhicule
- Option de trajet (course simple ou mise à disposition)
- Authentification pour clients -> liste des courses réservée
- Enregistrement des réservations et info clients dans Odoo
- Génération d'un bon de commande PDF contenant le récapitulatif de la réservation
- Envoi d'un email automatique depuis back-end en local
- Traduction sur toutes les pages 

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


