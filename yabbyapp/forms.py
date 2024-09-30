# yabbyapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Note, User

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'image', 'pdf']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')  # Adjust fields as needed