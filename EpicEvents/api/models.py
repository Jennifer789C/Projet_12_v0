from django.db import models
from django.conf import settings


class Client(models.Model):
    class Statut(models.TextChoices):
        Prospect = "Prospect"
        Client = "Client"

    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=25)
    email = models.EmailField()
    tel = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
    societe = models.CharField(max_length=250)
    statut = models.CharField(max_length=10, choices=Statut.choices)
    date_creation = models.DateField(auto_now_add=True)
    date_maj = models.DateField(auto_now=True)
    vendeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)


class Contrat(models.Model):
    ouvert = models.BooleanField(default=True)
    signe = models.BooleanField(default=False)
    date_signature = models.DateField()
    montant = models.FloatField()
    echeance = models.DateField()
    date_creation = models.DateField(auto_now_add=True)
    date_maj = models.DateField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


class Evenement(models.Model):
    ouvert = models.BooleanField(default=True)
    date_evenement = models.DateField()
    participants = models.PositiveIntegerField()
    notes = models.TextField()
    date_creation = models.DateField(auto_now_add=True)
    date_maj = models.DateField(auto_now=True)
    contrat = models.OneToOneField(Contrat, on_delete=models.CASCADE)
    support = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
