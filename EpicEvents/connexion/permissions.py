from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from api.models import Client, Evenement


class EstVendeur(BasePermission):
    def has_permission(self, request, view):
        groupe_vente = Group.objects.get(name="vente")
        if request.user.groups == groupe_vente:
            return True
        return False


class EstResponsableClient(BasePermission):
    def has_permission(self, request, view):
        client = Client.objects.get(id=view.kwargs["pk"])
        if request.user == client.vendeur:
            return True
        return False


class EstResponsableClientContrat(BasePermission):
    def has_permission(self, request, view):
        client = Client.objects.get(id=view.kwargs["client_pk"])
        if request.user == client.vendeur:
            return True
        return False


class EstResponsableEvenement(BasePermission):
    def has_permission(self, request, view):
        evenement = Evenement.objects.get(id=view.kwargs["pk"])
        if request.user == evenement.support:
            return True
        client = Client.objects.get(id=view.kwargs["client_pk"])
        if request.user == client.vendeur:
            return True
        return False


class EstSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser is True:
            return True
        return False
