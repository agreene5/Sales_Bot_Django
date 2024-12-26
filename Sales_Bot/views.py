from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import Preference, User_Input, Checkout

from .forms import PreferenceForm, UserInputForm

def index(request):

    form = PreferenceForm()

    Preferences = Preference.objects.all()

    if request.method == "POST":
        form = PreferenceForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("sales_screen")

    context = {"Preferences": Preferences, "PreferenceForm": form}

    return render(request, "preference_screen.html", context)

def sales_screen(request):

    form = UserInputForm()

    UserInput = User_Input.objects.all()

    if request.method == "POST":
        form = UserInputForm(request.POST)

        if form.is_valid():
            form.save()

        return redirect("checkout_screen")

    context = {"UserInput": UserInput, "UserInputForm": form}

    return render(request, "sales_screen.html", context)

def checkout_screen(request):
    if request.method == "POST":
        time_shopping = request.POST.get("time_shopping", 0.0)
        items_bought = request.POST.get("items_bought", 0)
        money_spent = request.POST.get("money_spent", 0)

        Checkout.objects.create(
            time_shopping=float(time_shopping),
            items_bought=int(items_bought),
            money_spent=int(money_spent)
        )

        context = {"time_spent": time_shopping, "items_bought": items_bought, "money_spent": money_spent}

        return render(request, "checkout_screen.html", context)
    return render(request, 'checkout_screen.html')
