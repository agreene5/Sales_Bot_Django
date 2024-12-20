from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name=""),

    path("sales_screen", views.sales_screen, name="sales_screen"),
]