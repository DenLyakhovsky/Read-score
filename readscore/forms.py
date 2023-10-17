from .models import Book
from django import forms


class StartReadingSessionForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all())


class EndReadingSessionForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all())
