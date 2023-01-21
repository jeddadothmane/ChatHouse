from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("authentification:home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			request.session['username'] = form.cleaned_data['username']
			if user is not None:
				login(request, user)
				return redirect("authentification:home")

	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

@login_required
def logout_request(request):
	logout(request)
	return redirect("authentification:login")

@login_required
def home(request):
    return render(request, 'home.html', {'username': request.user.username})

@login_required
def room(request, room):
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': request.user.username,
        'room': room,
        'room_details': room_details
    })

@login_required
def checkview(request):
    room = request.POST['room_name']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+request.user.username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+request.user.username)

@login_required
def send(request):
    message = request.POST['message']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=request.user, room=room_id)
    new_message.save()

@login_required
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})