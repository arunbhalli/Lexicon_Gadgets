from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Customer


class UserLogin(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password')



class CustomerForm(ModelForm):
    class Meta():
        model = Customer
        fields= '__all__'
        exclude=['user']
    
