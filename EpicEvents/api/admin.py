from django.contrib import admin
from .models import Client, Contrat, Evenement


class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "societe", "statut", "vendeur")


admin.site.register(Client, ClientAdmin)


class ContratAdmin(admin.ModelAdmin):
    list_display = ("id", "ouvert", "signe", "client")


admin.site.register(Contrat, ContratAdmin)


class EvenementAdmin(admin.ModelAdmin):
    list_display = ("id", "ouvert", "contrat", "support")


admin.site.register(Evenement, EvenementAdmin)
