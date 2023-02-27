from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import pytest

Personnel = get_user_model()


@pytest.mark.django_db
def test_list_client_sans_authentification(apiclient):
    reponse = apiclient.get("/client/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_list_client_avec_authentification(apiclient, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get("/client/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200


@pytest.mark.django_db
def test_retrieve_client_sans_authentification(apiclient, client):
    reponse = apiclient.get("/client/1/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_retrieve_client_avec_authentification(apiclient, client, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get(f"/client/{client.id}/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200


@pytest.mark.django_db
def test_create_client_sans_authentification(apiclient):
    reponse = apiclient.post("/client/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_technicien"])
def test_create_client_sans_permission(apiclient, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.post("/client/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_create_client(apiclient, token_access_vendeur):
    data = {"societe": "Societe Test",
            "statut": "Prospect",
            "nom": "Nom Contact",
            "prenom": "Prenom Contact",
            "email": "client@test.fr",
            "tel": "0123456789",
            "port": "98.76.54.32.10"}
    reponse = apiclient.post("/client/",
                             data=data,
                             HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 201
    assert reponse.data["societe"] == "Societe Test"


@pytest.mark.django_db
def test_update_client_sans_authentification(apiclient):
    reponse = apiclient.put("/client/1/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_technicien"])
def test_update_client_sans_permission(apiclient, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.put("/client/1/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_update_client_bon_vendeur(apiclient, token_access_vendeur, client):
    data = {"societe": "Societe Modifiée",
            "statut": "Prospect",
            "nom": "Nom Contact",
            "prenom": "Prenom Contact",
            "email": "client@test.fr",
            "tel": "0123456789",
            "port": "98.76.54.32.10"}
    reponse = apiclient.put(f"/client/{client.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200
    assert reponse.data["societe"] == "Societe Modifiée"


@pytest.mark.django_db
def test_update_client_mauvais_vendeur(apiclient, client):
    data = {"societe": "Societe Modifiée",
            "statut": "Prospect",
            "nom": "Nom Contact",
            "prenom": "Prenom Contact",
            "email": "client@test.fr",
            "tel": "0123456789"}
    vendeur = Personnel.objects.create_user(email="vendeur2@mail.fr", password="test")
    groupe_vente = Group.objects.get(name="vente")
    groupe_vente.user_set.add(vendeur)
    vendeur.save()

    reponse = apiclient.post("/login/",
                             data={"email": vendeur.email,
                                   "password": "test"},
                             )
    token = reponse.data["access"]

    reponse = apiclient.put(f"/client/{client.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_destroy_client_sans_authentification(apiclient):
    reponse = apiclient.delete("/client/1/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_destroy_client(apiclient, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.delete("/client/1/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 405 or 403
