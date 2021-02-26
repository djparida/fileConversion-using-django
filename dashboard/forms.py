from django import forms
from .models import Order, fileConversion
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = fileConversion
        fields = ['myfile', 'user']
    
