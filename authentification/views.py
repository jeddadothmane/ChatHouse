# Importation des formulaires, des messages de Django, des fonctions d'authentification,
# des redirections, des modèles et des réponses JSON
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Fonction pour gérer les demandes d'enregistrement:
def register_request(request):
    # Si la demande est de type POST
    if request.method == "POST":
        form = NewUserForm(request.POST)
        # Si le formulaire est valide
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("authentification:home")
    # Créez une instance de NewUserForm si la demande est de type GET
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form})

# Fonction pour gérer les demandes de connexion:
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():    		# Si le formulaire est valide
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            request.session['username'] = form.cleaned_data['username']  # Ajoutez le nom d'utilisateur à la session
            if user is not None:
                login(request, user)
                return redirect("authentification:home")

    # Créez une instance de AuthenticationForm si la demande est de type GET
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

# Fonction pour gérer les demandes de déconnexion
@login_required
def logout_request(request):
    logout(request)
    return redirect("authentification:login")

# Fonction pour afficher la page d'accueil
@login_required
def home(request):
    return render(request, 'home.html', {'username': request.user.username})

# Fonction pour afficher la page de la salle de discussion
@login_required
def room(request, room):
    room_details = Room.objects.get(name=room)   # Récupérer les détails de la salle en utilisant le nom de la salle
    return render(request, 'room.html', {
        'username': request.user.username,
        # Passer le nom de la salle et les détails de la salle au contexte
        'room': room,
        'room_details': room_details
    })

#Fonction pour vérifier l'existence d'une salle de discussion
@login_required
def check_room(request):
    room = request.POST['room_name']
    if Room.objects.filter(name=room).exists(): # Vérifiez si une salle existe déjà avec ce nom
        return redirect('/'+room+'/?username='+request.user.username)
    else:
        new_room = Room.objects.create(name=room)     # Créer une nouvelle salle de discussion et la sauvegarder en base de données
        new_room.save()
        return redirect('/'+room+'/?username='+request.user.username)

#Fonction pour envoyer un message
@login_required
def send(request):
    message = request.POST['message']
    room_id = request.POST['room_id']
    # Créer un nouveau message et le sauvegarder en base de données
    new_message = Message.objects.create(value=message, user=request.user, room=room_id)
    new_message.save()

#Fonction pour récupérer les messages
@login_required
def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    # Récupérer tous les messages de la salle de discussion
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})