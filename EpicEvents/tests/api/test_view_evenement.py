from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.exceptions import ErrorDetail
import pytest

Personnel = get_user_model()


@pytest.mark.django_db
def test_list_evenement_sans_authentification(apiclient, contrat):
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/{contrat.id}/evenement/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_list_evenement(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/{contrat.id}/evenement/",
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200


@pytest.mark.django_db
def test_retrieve_evenement_sans_authentification(apiclient, evenement):
    reponse = apiclient.get(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/")
    assert reponse.status_code == 401


@pytest.mark.django_db
def test_retrieve_evenement_sans_permission(apiclient, evenement, token_access_gestionnaire):
    reponse = apiclient.get(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            HTTP_AUTHORIZATION="Bearer "+token_access_gestionnaire)
    assert reponse.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_vendeur",
                                   "token_access_technicien"])
def test_retrieve_evenement(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200


@pytest.mark.django_db
def test_retrieve_evenement_mauvais_vendeur(apiclient, evenement):
    vendeur = Personnel.objects.create_user(email="vendeur2@mail.fr", password="test")
    groupe_vente = Group.objects.get(name="vente")
    groupe_vente.user_set.add(vendeur)
    vendeur.save()
    reponse = apiclient.post("/login/",
                             data={"email": vendeur.email,
                                   "password": "test"},
                             )
    token = reponse.data["access"]

    reponse = apiclient.get(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_retrieve_evenement_mauvais_technicien(apiclient, evenement):
    technicien = Personnel.objects.create_user(email="technicien2@mail.fr", password="test")
    groupe_support = Group.objects.get(name="support")
    groupe_support.user_set.add(technicien)
    technicien.save()
    reponse = apiclient.post("/login/",
                             data={"email": technicien.email,
                                   "password": "test"},
                             )
    token = reponse.data["access"]

    reponse = apiclient.get(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_create_evenement_sans_authentification(apiclient, contrat):
    reponse = apiclient.post(f"/client/{contrat.client.id}/contrat/{contrat.id}/evenement/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_technicien"])
def test_create_evenement_sans_permission(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.post(f"/client/{contrat.client.id}/contrat/{contrat.id}/evenement/",
                             HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403 or 405


@pytest.mark.django_db
def test_create_evenement(apiclient, contrat, token_access_vendeur):
    data = {"date_evenement": "2023-06-16",
            "participants": 30}
    reponse = apiclient.post(f"/client/{contrat.client.id}/contrat/{contrat.id}/evenement/",
                             data=data,
                             HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 201


@pytest.mark.django_db
def test_create_evenement_mauvais_vendeur(apiclient, contrat):
    vendeur = Personnel.objects.create_user(email="vendeur2@mail.fr", password="test")
    groupe_vente = Group.objects.get(name="vente")
    groupe_vente.user_set.add(vendeur)
    vendeur.save()
    reponse = apiclient.post("/login/",
                             data={"email": vendeur.email,
                                   "password": "test"},
                             )
    token = reponse.data["access"]

    data = {"date_evenement": "2023-06-16",
            "participants": 30}
    reponse = apiclient.post(f"/client/{contrat.client.id}/contrat/{contrat.id}/evenement/",
                             data=data,
                             HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_update_evenement_sans_authentification(apiclient, evenement):
    reponse = apiclient.put(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/")
    assert reponse.status_code == 401


@pytest.mark.django_db
def test_update_evenement_sans_permission(apiclient, evenement, token_access_gestionnaire):
    reponse = apiclient.put(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            HTTP_AUTHORIZATION="Bearer "+token_access_gestionnaire)
    assert reponse.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_vendeur",
                                   "token_access_technicien"])
def test_update_evenement(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    data = {"ouvert": True,
            "date_evenement": "2023-06-16",
            "participants": 30,
            "notes": "en plein air"}
    reponse = apiclient.put(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200


@pytest.mark.django_db
def test_update_evenement_mauvais_vendeur(apiclient, evenement):
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
            "date_evenement": "2023-06-16",
            "participants": 30,
            "notes": "en plein air"}
    reponse = apiclient.put(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_update_evenement_mauvais_technicien(apiclient, evenement):
    technicien = Personnel.objects.create_user(email="technicien2@mail.fr", password="test")
    groupe_support = Group.objects.get(name="support")
    groupe_support.user_set.add(technicien)
    technicien.save()
    reponse = apiclient.post("/login/",
                             data={"email": technicien.email,
                                   "password": "test"},
                             )
    token = reponse.data["access"]

    data = {"ouvert": True,
            "date_evenement": "2023-06-16",
            "participants": 30,
            "notes": "en plein air"}
    reponse = apiclient.put(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_vendeur",
                                   "token_access_technicien"])
def test_update_evenement_ferme(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    data = {"ouvert": False,
            "date_evenement": "2023-06-16",
            "participants": 30}
    reponse = apiclient.put(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.data["ouvert"] is False
    reponse = apiclient.put(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                            data=data,
                            HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 400
    assert reponse.data == [ErrorDetail(string='Votre évènement est fermé, vous ne pouvez plus le modifier.', code='invalid')]


@pytest.mark.django_db
def test_destroy_evenement_sans_authentification(apiclient, evenement):
    reponse = apiclient.delete(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_destroy_evenement_sans_permission(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.delete(f"/client/{evenement.contrat.client.id}/contrat/{evenement.contrat.id}/evenement/{evenement.id}/",
                               HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403 or 405
