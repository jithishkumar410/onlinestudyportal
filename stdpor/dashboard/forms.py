from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['title','des']

class DashboardForm(forms.Form):
    text=forms.CharField(max_length=100,label="Please enter your search")

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_finished']

class UserRegistration(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']
