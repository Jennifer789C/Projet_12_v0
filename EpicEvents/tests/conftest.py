from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import pytest
from rest_framework.test import APIClient
from api.models import Client, Contrat

Personnel = get_user_model()


@pytest.fixture()
def apiclient():
    return APIClient()


@pytest.fixture()
def gestionnaire():
    gestionnaire = Personnel.objects.create_user(email="gestionnaire@mail.fr", password="test")
    groupe_gestion = Group.objects.get(name="gestion")
    groupe_gestion.user_set.add(gestionnaire)
    gestionnaire.save()
    return gestionnaire


@pytest.fixture()
def token_access_gestionnaire(apiclient, gestionnaire):
    reponse = apiclient.post("/login/",
                             data={"email": gestionnaire.email,
                                   "password": "test"},
                             )
    return reponse.data["access"]


@pytest.fixture()
def vendeur():
    vendeur = Personnel.objects.create_user(email="vendeur@mail.fr", password="test")
    groupe_vente = Group.objects.get(name="vente")
    groupe_vente.user_set.add(vendeur)
    vendeur.save()
    return vendeur


@pytest.fixture()
def token_access_vendeur(apiclient, vendeur):
    reponse = apiclient.post("/login/",
                             data={"email": vendeur.email,
                                   "password": "test"},
                             )
    return reponse.data["access"]


@pytest.fixture()
def technicien():
    technicien = Personnel.objects.create_user(email="technicien@mail.fr", password="test")
    groupe_support = Group.objects.get(name="support")
    groupe_support.user_set.add(technicien)
    technicien.save()
    return technicien


@pytest.fixture()
def token_access_technicien(apiclient, technicien):
    reponse = apiclient.post("/login/",
                             data={"email": technicien.email,
                                   "password": "test"},
                             )
    return reponse.data["access"]


@pytest.fixture()
def client(vendeur):
    client = Client.objects.create(nom="NomTest", prenom="PrenomTest",
                                   email="mail@test.fr", tel="0123456789",
                                   societe="SteTest", statut="Client",
                                   vendeur=vendeur)
    return client


@pytest.fixture()
def contrat(client):
    contrat = Contrat.objects.create(montant=500, echeance="2023-03-31",
                                     client=client)
    return contrat
