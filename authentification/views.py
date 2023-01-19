from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("authentification:home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("authentification:login")

@login_required
def home(request):
    return render(request, 'home.html', {'username': request.user.username})

@login_required
def room(request, room):
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', context = {
        'username': request.user.username,
        'room': room,
        'room_details': room_details,
        'user': request.user,
        'room_id': room_details.id,
        'user_id': request.user.id
    }
)

@login_required
def checkview(request):
    room = request.POST['room_name']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+request.user.username)
    else:
        new_room = Room.objects.create(name=room, creator=request.user)
        new_room.save()
        return redirect('/'+room+'/?username='+request.user.username)

@login_required
def send(request):
    message = request.POST['message']
    room_id = request.POST['room_id']
    new_message = Message.objects.create(value=message, user=request.user, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

@login_required
def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})


@login_required
def delete_room(request, room_id):
    room = Room.objects.get(pk=room_id)

    # Check if the current user is the creator of the room
    if request.user == room.creator:
        # Delete the room
        room.delete()
        messages.info(request, f"Room {room.name} has been deleted.")
    else:
        messages.error(request, "You do not have permission to delete the room.")

    return redirect('authentification:home')
