
from django import forms
from django.forms import ModelForm

from .models import Preference, User_Input

class PreferenceForm(forms.ModelForm):

    items_likes = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Please enter what items you like"}))
    items_dislikes = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Please enter what items you dislike"}))

    class Meta:
        model = Preference
        fields = "__all__"

class UserInputForm(forms.ModelForm):

    user_input = forms.CharField(widget=forms.Textarea(attrs={"placeholder":""}))
    class Meta:
        model = User_Input
        fields = "__all__"