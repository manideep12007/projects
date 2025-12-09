from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Room,Message,Hashtag
from .forms import RoomForm,MessageForm,HashtagForm


def home(request):
    q = request.GET.get("q")
    if q:
        rooms = Room.objects.filter(
            Q(name__icontains=q) | 
            Q(hashtag__name__icontains=q) |
            Q(information__icontains=q)
        )
    else:
        rooms = Room.objects.all().order_by("-updated")
    hashtags = Hashtag.objects.all().order_by("name")
    count = rooms.count()
    context = {
        "rooms":rooms,
        "hashtags":hashtags,
        "count":count
    }
    return render(request,"base/home.html",context)

@login_required(login_url='login')
def create_room(request):
    action = "create"
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            next_page = request.GET.get('next','home')
            return redirect(next_page)
    else:
        form = RoomForm()
    context = {
        "action":action,
        "form":form,
    }
    return render(request,"base/room_form.html",context)

@login_required(login_url='login')
def update_room(request,pk):
    action = "update"
    room = get_object_or_404(Room,pk=pk)
    if request.user != room.host:
        return HttpResponseForbidden("Only owner can update this room")
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            next_page = request.GET.get('next','home')
            return redirect(next_page)
    else:
        form = RoomForm(instance=room)
    context = {
        "action":action,
        "form":form,
    }
    return render(request,"base/room_form.html",context)

@login_required(login_url='login')
def delete_room(request,pk):
    action = "delete"
    room = get_object_or_404(Room,pk=pk)
    if request.user != room.host:
        return HttpResponseForbidden("Only owner can delete this room")
    if request.method == "POST":
        room.delete() 
        next_page = request.GET.get('next','home')
        return redirect(next_page)
    context = {
        "action":action,'room':room,
    }
    return render(request,"base/room_form.html",context)

def room(request,pk):
    room = get_object_or_404(Room,pk=pk)
    participants = room.participants.all()
    room_messages = room.message_set.all().select_related("user")
    participants_count = participants.count()
    if request.method == "POST":
        chat = request.POST.get('chat').strip()
        if not chat:
            return render(request, "base/room.html", {"room": room, "room_messages": room_messages, "participants": participants}, status=400)
        if chat:
            message = Message.objects.create(
                        room=room,
                        user=request.user,
                        chat=chat
            ) 
            room.participants.add(message.user)
            return redirect("room",room.id)         
    context = {
        "room":room,
        "room_messages":room_messages,
        "participants":participants,
        "participants_count":participants_count
    }
    return render(request,"base/room.html",context)

@login_required(login_url="login")
def delete_message(request, pk):
    room_message = get_object_or_404(Message, pk=pk)
    if request.user != room_message.user and not request.user.is_superuser:
        return HttpResponseForbidden("Only the message owner or a superuser can delete this message.")
    room_id = room_message.room.id
    room_message.delete()
    return redirect("room", pk=room_id)

@login_required(login_url='login')
def update_message(request,pk):
    room_message = get_object_or_404(Message,pk=pk)
    if request.user != room_message.user:
        return HttpResponseForbidden("Only message owner can update this message.")
    if request.method == "POST":
        form = MessageForm(request.POST,instance=room_message)
        if form.is_valid():
            form.save()
            next_page = request.GET.get("name","room")
            return redirect(next_page,pk=room_message.room.id)
    else:
        form = MessageForm(instance=room_message)
    context = {"form":form}
    return render(request,"base/message_form.html",context)

@login_required(login_url='login')
def create_hashtag(request):
    if not request.user.is_superuser:
        return render(request, "base/403.html", {"message": "Only superuser can create hashtags"}, status=403)
    if request.method == "POST":
        form = HashtagForm(request.POST)
        if form.is_valid():
            form.save()
            next_page = request.GET.get("next", "home")
            if not next_page.startswith('/'):
                next_page = 'home'
            return redirect(next_page)
    else:
        form = HashtagForm()
    context = {"form": form}
    return render(request, "base/hashtag_form.html", context)

@login_required(login_url='login')
def delete_hashtag(request,pk):
    hashtag = get_object_or_404(Hashtag,pk=pk)
    if not request.user.is_superuser:
        return render(request, "base/403.html", {"message": "Only superuser can create hashtags"}, status=403)
    hashtag.delete()
    next_page = request.GET.get("next","home")
    return redirect(next_page)

