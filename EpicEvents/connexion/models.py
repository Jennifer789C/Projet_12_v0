from django.db import models
from django.contrib.auth.models import AbstractUser


class Personnel(AbstractUser):
    first_name = None
    last_name = None
    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=25)
    tel = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
