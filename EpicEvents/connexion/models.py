from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class Personnel(AbstractUser):
    GESTION = "GESTION"
    VENTE = "VENTE"
    SUPPORT = "SUPPORT"

    CHOIX = (
        (GESTION, "Gestion"),
        (VENTE, "Vente"),
        (SUPPORT, "Support")
    )

    first_name = None
    last_name = None
    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=25)
    tel = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
    equipe = models.CharField(max_length=10, choices=CHOIX)
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.prenom

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.equipe == self.GESTION:
            self.is_staff = True
            groupe = Group.objects.get(name="gestion")
            groupe.user_set.add(self)
        elif self.equipe == self.VENTE:
            groupe = Group.objects.get(name="vente")
            groupe.user_set.add(self)
        elif self.equipe == self.SUPPORT:
            groupe = Group.objects.get(name="support")
            groupe.user_set.add(self)
