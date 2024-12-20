from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import Preference

from .forms import PreferenceForm

def index(request):

    form = PreferenceForm()

    Preferences = Preference.objects.all()

    if request.method == "POST":
        form = PreferenceForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("/")

    context = {"Preferences": Preferences, "PreferenceForm": form}

    return render(request, "preference_screen.html", context)

def sales_screen(request):
    return render(request, "sales_screen.html")