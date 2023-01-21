
# Importation des modules nécessaires pour gérer les URL
from django.urls import path
from . import views

app_name = "authentification"       # Nom de l'application pour les URL

urlpatterns = [
    path("logout", views.logout_request, name="logout"),        # URL pour déconnecter l'utilisateur
    path("", views.login_request, name="login"),                # URL pour afficher la page de connexion
    path('home/', views.home, name='home'),                     # URL pour afficher la page d'accueil
    path('home/check_room', views.check_room, name='check_room'),       # URL pour vérifier l'existence d'une salle de discussion
    path("register/", views.register_request, name="register"),             # URL pour afficher la page d'enregistrement
    path("login/", views.login_request, name="login"),          # URL pour traiter les demandes de connexion
    path('<str:room>/', views.room, name='room'),               # URL pour afficher la page de la salle de discussion
    path('send', views.send, name='send'),                      # URL pour envoyer un message
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),     # URL pour récupérer les messages
]