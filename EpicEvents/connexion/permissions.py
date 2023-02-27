from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from api.models import Client


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
