from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.exceptions import ErrorDetail
import pytest

Personnel = get_user_model()


@pytest.mark.django_db
def test_list_contrat_sans_authentification(apiclient, client):
    reponse = apiclient.get(f"/client/{client.id}/contrat/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_technicien"])
def test_list_contrat_sans_permission(apiclient, client, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get(f"/client/{client.id}/contrat/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_list_contrat(apiclient, client, token_access_vendeur):
    reponse = apiclient.get(f"/client/{client.id}/contrat/",
                            HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200


@pytest.mark.django_db
def test_retrieve_contrat_sans_authentification(apiclient, contrat):
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/{contrat.id}/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_technicien"])
def test_retrieve_contrat_sans_permission(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_retrieve_contrat(apiclient, contrat, token_access_vendeur):
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                            HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200


@pytest.mark.django_db
def test_create_contrat_sans_authentification(apiclient, client):
    reponse = apiclient.post(f"/client/{client.id}/contrat/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_technicien"])
def test_create_contrat_sans_permission(apiclient, client, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.post(f"/client/{client.id}/contrat/",
                             HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_create_contrat(apiclient, client, token_access_vendeur):
    data = {"montant": 950,
            "echeance": "2023-07-05"}
    reponse = apiclient.post(f"/client/{client.id}/contrat/",
                             data=data,
                             HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 201


@pytest.mark.django_db
def test_create_contrat_mauvais_vendeur(apiclient, client):
    vendeur = Personnel.objects.create_user(email="vendeur2@mail.fr", password="test")
    groupe_vente = Group.objects.get(name="vente")
    groupe_vente.user_set.add(vendeur)
    vendeur.save()
    reponse = apiclient.post("/login/",
                             data={"email": vendeur.email,
                                   "password": "test"},
                             )
    token = reponse.data["access"]

    data = {"montant": 950,
            "echeance": "2023-07-05"}
    reponse = apiclient.post(f"/client/{client.id}/contrat/",
                             data=data,
                             HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_create_contrat_prospect(apiclient, token_access_vendeur):
    data = {"societe": "Societe Test",
            "statut": "Prospect",
            "nom": "Nom Contact",
            "prenom": "Prenom Contact",
            "email": "client@test.fr",
            "tel": "0123456789"}
    reponse = apiclient.post("/client/",
                             data=data,
                             HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    client = reponse.data["id"]

    data = {"montant": 950,
            "echeance": "2023-07-05"}
    reponse = apiclient.post(f"/client/{client}/contrat/",
                             data=data,
                             HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 400
    assert reponse.data == [ErrorDetail(string="Le client doit être au statut 'Client'.", code='invalid')]


@pytest.mark.django_db
def test_update_contrat_sans_authentification(apiclient, contrat):
    reponse = apiclient.put(f"/client/{contrat.client.id}/contrat/{contrat.id}/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_technicien"])
def test_update_contrat_sans_permission(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.put(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_update_contrat(apiclient, contrat, token_access_vendeur):
    data = {"ouvert": True,
            "signe": False,
            "date_signature": "",
            "montant": 1050,
            "echeance": "2023-07-31"}
    reponse = apiclient.put(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200
    assert reponse.data["montant"] == 1050


@pytest.mark.django_db
def test_update_contrat_mauvais_vendeur(apiclient, contrat):
    vendeur = Personnel.objects.create_user(email="vendeur2@mail.fr", password="test")
    groupe_vente = Group.objects.get(name="vente")
    groupe_vente.user_set.add(vendeur)
    vendeur.save()
    reponse = apiclient.post("/login/",
                             data={"email": vendeur.email,
                                   "password": "test"},
                             )
    token = reponse.data["access"]

    data = {"ouvert": True,
            "signe": False,
            "date_signature": "",
            "montant": 1050,
            "echeance": "2023-07-31"}
    reponse = apiclient.put(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer " + token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_update_contrat_ferme(apiclient, contrat, token_access_vendeur):
    data = {"ouvert": False,
            "signe": False,
            "date_signature": "",
            "montant": 1050,
            "echeance": "2023-07-31"}
    reponse = apiclient.put(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer " + token_access_vendeur)
    assert reponse.data["ouvert"] is False
    reponse = apiclient.put(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer " + token_access_vendeur)
    assert reponse.status_code == 400
    assert reponse.data == [ErrorDetail(string='Votre contrat est fermé, vous ne pouvez plus le modifier.', code='invalid')]


@pytest.mark.django_db
def test_update_contrat_erreur_signature(apiclient, contrat, token_access_vendeur):
    data = {"ouvert": False,
            "signe": True,
            "date_signature": "",
            "montant": 1050,
            "echeance": "2023-07-31"}
    reponse = apiclient.put(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 400
    assert reponse.data["non_field_errors"] == [ErrorDetail(
        string='Votre contrat signé doit contenir une date de signature.',
        code='invalid')]

    data = {"ouvert": False,
            "signe": False,
            "date_signature": "2023-02-17",
            "montant": 1050,
            "echeance": "2023-07-31"}
    reponse = apiclient.put(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 400
    assert reponse.data["non_field_errors"] == [ErrorDetail(
        string="Votre contrat ne peut pas contenir de date de signature s'il n'est pas signé.",
        code='invalid')]


@pytest.mark.django_db
def test_destroy_contrat_sans_authentification(apiclient, contrat):
    reponse = apiclient.delete(f"/client/{contrat.client.id}/contrat/{contrat.id}/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_destroy_contrat_sans_permission(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.delete(f"/client/{contrat.client.id}/contrat/{contrat.id}/",
                               HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403
