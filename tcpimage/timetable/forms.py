from django.forms import ModelForm
from django import forms
from .models import Picture


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'
        labels = {'photo': ''}
        textwrap = {'No file chosen': ''}
