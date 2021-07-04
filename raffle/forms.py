from django import forms
from .models import *

class CreatRaffleForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['event_name_text']

    persons = forms.ModelMultipleChoiceField(
        queryset=Person.objects.all().filter(active=True),
        initial=Person.objects.all().filter(active=True),
        widget=forms.CheckboxSelectMultiple
    )
