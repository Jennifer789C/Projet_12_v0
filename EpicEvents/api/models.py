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
    port = models.CharField(max_length=20, blank=True, null=True)
    societe = models.CharField(max_length=250)
    statut = models.CharField(max_length=10, choices=Statut.choices)
    date_creation = models.DateField(auto_now_add=True)
    date_maj = models.DateField(auto_now=True)
    vendeur = models.ForeignKey(settings.AUTH_USER_MODEL,
                                limit_choices_to={"groups": 2},
                                null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.societe


class Contrat(models.Model):
    ouvert = models.BooleanField(default=True)
    signe = models.BooleanField(default=False)
    date_signature = models.DateField(blank=True, null=True)
    montant = models.FloatField()
    echeance = models.DateField()
    date_creation = models.DateField(auto_now_add=True)
    date_maj = models.DateField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        if self.ouvert:
            ouvert = "ouvert"
        else:
            ouvert = "fermé"
        if self.signe:
            signe = f"signé le {self.date_signature}."
        else:
            signe = "non signé."
        return f"Contrat {ouvert} pour le client {self.client} : {signe}"


class Evenement(models.Model):
    ouvert = models.BooleanField(default=True)
    date_evenement = models.DateField()
    participants = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    date_creation = models.DateField(auto_now_add=True)
    date_maj = models.DateField(auto_now=True)
    contrat = models.OneToOneField(Contrat, on_delete=models.CASCADE)
    support = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.ouvert:
            ouvert = "ouvert"
        else:
            ouvert = "fermé"
        return f"Évènement du {self.date_evenement} : {ouvert}."
