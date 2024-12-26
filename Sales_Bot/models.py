from django.db import models
from django.contrib.auth.models import User

class Preference(models.Model):

    items_likes = models.CharField(max_length=1000)
    items_dislikes = models.CharField(max_length=1000)

    def __str__(self):
        return f"Liked items: {self.items_likes} || \n \
                 Disliked items: {self.items_dislikes}"

class User_Input(models.Model):

    user_input = models.CharField(max_length=1000)
    def __str__(self):
        return self.user_input

class Checkout(models.Model):

    time_shopping = models.FloatField()
    items_bought = models.IntegerField()
    money_spent = models.IntegerField()

    def __str__(self):
        return (f"Time shopped: {self.time_shopping}\nItems bought: {self.items_bought}\nMoney spent: {self.money_spent}")
