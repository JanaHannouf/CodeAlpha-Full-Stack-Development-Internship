from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Enter your email address"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm your password"}))
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter your full name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Enter your email address"}))
    
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'image']
