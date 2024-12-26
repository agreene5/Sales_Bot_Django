from django.contrib import admin

from .models import Preference, User_Input, Checkout

admin.site.register(Preference)

admin.site.register(User_Input)

admin.site.register(Checkout)