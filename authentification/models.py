# Importation des modules nécessaires pour gérer les modèles de base de données
from django.db import models
from datetime import datetime #module pour avoir la date et le temps

# Définition de la classe de modèle de salle de discussion
class Room(models.Model):
    # Nom de la salle de discussion
    name = models.CharField(max_length=1000)

# Définition de la classe de modèle de message
class Message(models.Model):
    # Salle de discussion associée au message
    room = models.CharField(max_length=1000)
    # Utilisateur qui a envoyé le message
    user = models.CharField(max_length=1000)
    # Contenu du message
    value = models.CharField(max_length=1000000)
    # Date et heure à laquelle le message a été envoyé
    date = models.DateTimeField(default=datetime.now, blank=True)
