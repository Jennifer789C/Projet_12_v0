from rest_framework.viewsets import ModelViewSet
from . import serializers
from .models import Client, Contrat, Evenement


class ClientViewset(ModelViewSet):
    http_method_names = ["get", "post", "put"]

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "list":
            return serializers.ClientListeSerializer
        return serializers.ClientDetailSerializer
