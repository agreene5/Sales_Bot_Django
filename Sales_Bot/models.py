from django.db import models

class Preference(models.Model):
    items_likes = models.CharField(max_length=1000)
    items_dislikes = models.CharField(max_length=1000)

    def __str__(self):
        return f"Liked items: {self.items_likes} | Disliked items: {self.items_dislikes}"

class User_Input(models.Model):
    user_input = models.CharField(max_length=1000)
    llm_response = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user_input

class Checkout(models.Model):
    time_shopping = models.FloatField()
    items_bought = models.IntegerField()
    money_spent = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Time shopped: {self.time_shopping}s | Items: {self.items_bought} | Spent: ${self.money_spent}"