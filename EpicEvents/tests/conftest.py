import pytest
from rest_framework.test import APIClient
from api.models import Client, Contrat


@pytest.fixture()
def client():
    client = Client.objects.create(nom="NomTest", prenom="PrenomTest",
                                   email="mail@test.fr", tel="0123456789",
                                   societe="SteTest", statut="Prospect")
    return client


@pytest.fixture()
def contrat(client):
    contrat = Contrat.objects.create(date_signature="2023-01-01", montant=500,
                                     echeance="2023-03-31", client=client)
    return contrat


@pytest.fixture()
def apiclient():
    return APIClient()
