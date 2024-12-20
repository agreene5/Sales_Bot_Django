from django.db import models
from django.contrib.auth.models import User

class Preference(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preference")
    items_likes = models.CharField(max_length=1000)
    items_dislikes = models.CharField(max_length=1000)

    def __str__(self):
        return f"Liked items: {self.items_likes} || \n \
                Disliked items: {self.items_dislikes}"