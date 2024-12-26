from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name=""),

    path("sales_screen", views.sales_screen, name="sales_screen"),

    path("checkout_screen", views.checkout_screen, name="checkout_screen")
]