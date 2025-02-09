from django import forms
from django.contrib.auth.models import User

class UserRegistrationCreationForm(forms.ModelForm):

    password1 = forms.CharField(max_length=100,widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100,widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email']
    
    def clean_password2(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')
        if password != confirm_password:
            raise forms.ValidationError('Passwords don\'t match')
        return cleaned_data
    

