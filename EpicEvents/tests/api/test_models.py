import pytest
from api.models import Client, Contrat, Evenement


@pytest.mark.django_db
def test_modele_client():
    client = Client.objects.create(nom="NomTest", prenom="PrenomTest",
                                   email="mail@test.fr", tel="0123456789",
                                   societe="SteTest", statut="Prospect")
    assert str(client) == "SteTest"


@pytest.mark.django_db
def test_modele_contrat(client):
    contrat = Contrat.objects.create(date_signature="2023-01-01", montant=500,
                                     echeance="2023-03-31", client=client)
    assert str(contrat) == "Contrat ouvert pour le client SteTest : non signé."


@pytest.mark.django_db
def test_modele_evenement(contrat):
    evenement = Evenement.objects.create(date_evenement="2023-02-12",
                                         participants=25, contrat=contrat)
    assert str(evenement) == "Évènement du 2023-02-12 : ouvert."
