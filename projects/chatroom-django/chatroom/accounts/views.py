from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import RoomUser
from .forms import AuthenticationRoomUserForm,CreationRoomUserForm,ProfileForm

def logout_user(request):
    logout(request)
    return redirect("home")

def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        form = AuthenticationRoomUserForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request,
                    username=username,
                    password=password)
            if user is not None:
                login(request,user=user)
                messages.success(request,"You logged in successfully!")
                next_page = request.GET.get("next", "home")
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request,"Please correct the errors in the form")
    else:
        form = AuthenticationRoomUserForm()
    context = {"form":form}
    return render(request,"accounts/login.html",context)

def signup_user(request):
    if request.method == "POST":
        form = CreationRoomUserForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            messages.success(request,"You logged in successfully!")
            next_page = request.GET.get('next','home')
            return redirect(next_page)
        else:
            messages.error(request, "There were errors in the form submission. Please check the fields.")
            print(form.errors)
    else:
        form = CreationRoomUserForm()
    context = {"form":form}
    return render(request,"accounts/signup.html",context)

def profile_view(request,pk):
    profile = get_object_or_404(RoomUser,pk=pk)
    hosted_rooms = profile.room_set.all().order_by('-updated')
    recent_messages = profile.message_set.select_related('room').order_by('-created')[:10]
    context = {
        "profile":profile,
        "hosted_rooms": hosted_rooms,
        "recent_messages": recent_messages
    }
    return render(request,"accounts/profile.html",context)

def update_profile(request,pk):
    if request.user.pk != pk:
        messages.error(request, "You are not authorized to update this profile.")
        return redirect("home")
    profile = get_object_or_404(RoomUser,pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            next_page = request.GET.get('next','home')
            return redirect(next_page)
        else:
            messages.error(request, "There were errors in the form submission. Please check the fields.")
    else:
        form = ProfileForm(instance=profile)
    context = {"form":form}
    return render(request,"accounts/profile_form.html",context)