from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from datetime import date
from .models import RoomUser

class AuthenticationRoomUserForm(AuthenticationForm):
    username = forms.CharField(max_length=250,
                    label="Username",
                    widget=forms.TextInput(attrs={
                        "placeholder":"Enter your Username",
                        "class": "form-control"
                    }))
    password = forms.CharField(label="Password",
                widget=forms.PasswordInput(
                attrs={"placeholder":"Enter your password",
                       "class":"form-control",
                        "type":"password"
                }))

class CreationRoomUserForm(UserCreationForm):
    profile_pic = forms.ImageField(required=False,label="Profile Image")
    email = forms.EmailField(label="Email",required=False,
                widget=forms.EmailInput(attrs={
                    'placeholder':'Enter your email id',
                    'class': 'form-control',
                }))
    GENDER_OPTIONS = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others')
    ]
    gender = forms.ChoiceField(label="Gender",
                choices=GENDER_OPTIONS,
                widget=forms.Select(
                attrs={"class":"form-conrol",
                }))
    dob = forms.DateField(label="Date of Birth",widget=forms.DateInput(
                attrs={
                    "type":"date","class":"form-control",
                }))
    bio = forms.CharField(label="Bio",widget=forms.Textarea(
                attrs={
                    "rows":4,
                    "placeholder":"Enter your bio",
                    "class": "form-control",
                }))
    username = forms.CharField(label="Username",widget=forms.TextInput(
                attrs={
                    "placeholder":"Enter your username",
                    "class":"form-control",
                }))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(
                attrs={
                    "type":"password",
                    "class":"form-control",
                    "placeholder":"Enter your password",
                }))
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(
                attrs={
                    "type":"password",
                    "class":"form-control",
                    "placeholder":"Confirm your password",
                }))
    class Meta:
        model = RoomUser
        fields = [
            "username", "email", "profile_pic", "dob", "bio", "gender",
            "password1", "password2"
        ]
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password2 != password1:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2
    
    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        if dob and dob > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return dob

    def clean_username(self):
        username = self.cleaned_data.get("username").lower()
        if RoomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("User already exists!")
        return username
    
class ProfileForm(forms.ModelForm):
    dob = forms.DateField(label="Date of birth",
                widget=forms.DateInput(attrs={"type":"date"}))
    profile_pic = forms.ImageField(required=False)
    class Meta:
        model = RoomUser
        fields = ["username","email","profile_pic",
                  "dob","bio","gender"]