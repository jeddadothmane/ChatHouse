from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

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
    return HttpResponse('Message sent successfully')

@login_required
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})
