from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationCreationForm

# user registration 
def register_form(request):
    if request.method == 'POST':
        form = UserRegistrationCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            login(request,user)
            return redirect('blog:home')
    else:
        form = UserRegistrationCreationForm()
    return render(request,'accounts/register.html',{'form':form})
# user login 
def login_form(request):
    if request.method =='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('blog:home')
        else:
            print('login failed')
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request,'accounts/login.html',{'form':form})
# user logout
def logout_form(request):
    logout(request)
    return redirect('blog:home')