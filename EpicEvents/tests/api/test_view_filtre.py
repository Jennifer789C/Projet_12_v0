import pytest


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_client_filtre_nom(apiclient, client, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get("/client/?nom=NomTest", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["societe"] == client.societe


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_client_filtre_email(apiclient, client, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get("/client/?email=mail@test.fr", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["societe"] == client.societe


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_client_filtre_nom_email(apiclient, client, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get("/client/?nom=NomTest&email=mail@test.fr", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["societe"] == client.societe
