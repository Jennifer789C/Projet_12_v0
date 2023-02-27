import pytest


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


"""
@pytest.mark.django_db
def test_create_client(apiclient):
    societe = "Societe Test"
    statut = "Prospect"
    nom = "Nom Contact"
    prenom = "Prenom Contact"
    reponse = apiclient.post("/client/", data={"societe": societe,
                                               "statut": statut,
                                               "nom": nom,
                                               "prenom": prenom})
    assert reponse.status_code == 201
    assert reponse.data["societe"] == societe
"""
