from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from . import serializers
from .models import Client, Contrat, Evenement
from connexion.permissions import EstVendeur, EstResponsableClient, EstResponsableClientContrat

Personnel = get_user_model()


class ClientViewset(ModelViewSet):
    http_method_names = ["get", "post", "put"]

    def get_queryset(self):
        return Client.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ClientListeSerializer
        elif self.action == "create" or self.action == "update":
            return serializers.ClientModifSerializer
        else:
            return serializers.ClientDetailSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAuthenticated]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, EstVendeur]
        elif self.action == "update":
            permission_classes = [IsAuthenticated, EstVendeur, EstResponsableClient]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        vendeur = Personnel.objects.get(id=self.request.user.id)
        client = serializer.save()
        client.vendeur = vendeur
        client.save()


class ContratViewset(ModelViewSet):
    http_method_names = ["get", "post", "put"]

    def get_queryset(self):
        return Contrat.objects.filter(client=self.kwargs["client_pk"]).order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ContratListeSerializer
        elif self.action == "create":
            return serializers.ContratCreationSerializer
        elif self.action == "update":
            return serializers.ContratModifSerializer
        else:
            return serializers.ContratDetailSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAuthenticated, EstVendeur]
        elif self.action == "create" or self.action == "update":
            permission_classes = [IsAuthenticated, EstVendeur, EstResponsableClientContrat]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
