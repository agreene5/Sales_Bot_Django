
from django import forms
from django.forms import ModelForm

from .models import Preference

class PreferenceForm(forms.ModelForm):

    items_likes = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Please enter what items you like"}))
    items_dislikes = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Please enter what items you dislike"}))

    class Meta:

        model = Preference
        fields = "__all__"