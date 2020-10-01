from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Python(models.Model):
    programmer = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    glossary  = models.BooleanField()
    simple = models.BooleanField()
    user_friendly = models.BooleanField()
    GUI = models.BooleanField()

    def __str__(self):
        return str(self.programmer)