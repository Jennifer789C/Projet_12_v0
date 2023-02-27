from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission


class EstGestionnaire(BasePermission):
    def has_permission(self, request, view):
        groupe_gestion = Group.objects.get(name="gestion")
        if request.user.groups == groupe_gestion:
            return True
        return False


class EstVendeur(BasePermission):
    def has_permission(self, request, view):
        groupe_vente = Group.objects.get(name="vente")
        if request.user.groups == groupe_vente:
            return True
        return False


class EstTechnicien(BasePermission):
    def has_permission(self, request, view):
        groupe_support = Group.objects.get(name="support")
        if request.user.groups == groupe_support:
            return True
        return False
