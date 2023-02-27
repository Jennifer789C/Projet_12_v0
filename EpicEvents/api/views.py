from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from . import serializers
from .models import Client, Contrat, Evenement
from connexion.permissions import EstGestionnaire, EstVendeur, EstTechnicien

Personnel = get_user_model()


class ClientViewset(ModelViewSet):
    http_method_names = ["get", "post", "put"]

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ClientListeSerializer
        elif self.action == "create" or self.action == "update":
            return serializers.ClientModifSerializer
        return serializers.ClientDetailSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        elif self.action == "create" or self.action == "update":
            permission_classes = [IsAuthenticated, EstVendeur]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        vendeur = Personnel.objects.get(id=self.request.user.id)
        client = serializer.save()
        client.vendeur.add(vendeur)
        client.save()
