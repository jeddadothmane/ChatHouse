
# Importation des modules nécessaires pour gérer les URL
from django.contrib import admin
from django.urls import path, include

# Liste des URL pour l'application
urlpatterns = [
    path('admin/', admin.site.urls),     # URL pour accéder à l'interface d'administration
    path('', include('authentification.urls')),     # URL pour inclure les URL de l'application d'authentification
]
