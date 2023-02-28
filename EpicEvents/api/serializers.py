from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Client, Contrat, Evenement


class ClientListeSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "societe", "statut", "nom", "prenom"]


class ClientDetailSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "societe", "statut", "nom", "prenom", "email", "tel",
                  "port", "date_creation", "date_maj", "vendeur"]


class ClientModifSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "societe", "statut", "nom", "prenom", "email", "tel",
                  "port"]


class ContratListeSerializer(ModelSerializer):
    parent_lookup_kwargs = {"client_pk": "client__pk"}

    class Meta:
        model = Contrat
        fields = ["id", "client", "ouvert", "signe"]


class ContratCreationSerializer(ModelSerializer):
    parent_lookup_kwargs = {"client_pk": "client__pk"}

    class Meta:
        model = Contrat
        fields = ["id", "montant", "echeance"]


class ContratModifSerializer(ModelSerializer):
    parent_lookup_kwargs = {"client_pk": "client__pk"}

    class Meta:
        model = Contrat
        fields = ["id", "ouvert", "signe", "date_signature",
                  "montant", "echeance"]

    def validate(self, data):
        if data["signe"] is True:
            if data["date_signature"] is None:
                raise ValidationError("Votre contrat signé doit contenir une date de signature.")
        else:
            if data["date_signature"] is not None:
                raise ValidationError("Votre contrat ne peut pas contenir de date de signature s'il n'est pas signé.")
        return data


class ContratDetailSerializer(ModelSerializer):
    parent_lookup_kwargs = {"client_pk": "client__pk"}

    class Meta:
        model = Contrat
        fields = ["id", "client", "ouvert", "signe", "date_signature",
                  "montant", "echeance", "date_creation", "date_maj"]


class EvenementListeSerializer(ModelSerializer):
    class Meta:
        model = Evenement
        fields = ["id", "ouvert", "date_evenement"]


class EvenementDetailSerializer(ModelSerializer):
    class Meta:
        model = Evenement
        fields = ["id", "ouvert", "date_evenement", "participants", "notes",
                  "date_creation", "date_maj", "contrat", "support"]
