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


@pytest.mark.django_db
def test_list_contrat_sans_authentification(apiclient):
    reponse = apiclient.get("/contrat/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_technicien"])
def test_list_contrat_sans_permission(apiclient, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get("/contrat/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_list_contrat(apiclient, token_access_vendeur):
    reponse = apiclient.get("/contrat/", HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200


@pytest.mark.django_db
def test_list_contrat_filtre_nom(apiclient, contrat, token_access_vendeur):
    reponse = apiclient.get("/contrat/?nom_client=NomTest", HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["client"] == contrat.client.id


@pytest.mark.django_db
def test_list_contrat_filtre_email(apiclient, contrat, token_access_vendeur):
    reponse = apiclient.get("/contrat/?email_client=mail@test.fr", HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["client"] == contrat.client.id


@pytest.mark.django_db
def test_list_contrat_filtre_date(apiclient, contrat, token_access_vendeur):
    reponse = apiclient.get("/contrat/?date=2023-08-07", HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 0


@pytest.mark.django_db
def test_list_contrat_filtre_date_via_client(apiclient, contrat, token_access_vendeur):
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/?date=2023-08-07", HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 0


@pytest.mark.django_db
def test_list_contrat_filtre_montant(apiclient, contrat, token_access_vendeur):
    reponse = apiclient.get("/contrat/?montant=500", HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["client"] == contrat.client.id


@pytest.mark.django_db
def test_list_contrat_filtre_montant_via_client(apiclient, contrat, token_access_vendeur):
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/?montant=500", HTTP_AUTHORIZATION="Bearer "+token_access_vendeur)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["client"] == contrat.client.id


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_retrieve_contrat(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get(f"/contrat/{contrat.id}/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_create_contrat(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.post(f"/contrat/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_update_contrat(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.put(f"/contrat/{contrat.id}/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_destroy_contrat(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.delete(f"/contrat/{contrat.id}/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_list_evenement_sans_authentification(apiclient):
    reponse = apiclient.get("/evenement/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_list_evenement(apiclient, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get("/evenement/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_list_evenement_filtre_nom(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get("/evenement/?nom_client=NomTest", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["contrat"] == evenement.contrat.id


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_list_evenement_filtre_email(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get("/evenement/?email_client=mail@test.fr", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["contrat"] == evenement.contrat.id


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_list_evenement_filtre_date(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get("/evenement/?date=2023-06-16", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 200
    assert reponse.data["count"] == 1
    assert reponse.data["results"][0]["contrat"] == evenement.contrat.id


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_retrieve_evenement(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get(f"/evenement/{evenement.id}/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_create_evenement(apiclient, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.post("/evenement/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_update_evenement(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.put(f"/evenement/{evenement.id}/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_vendeur",
                                   "token_access_technicien"])
def test_delete_evenement(apiclient, evenement, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.delete(f"/evenement/{evenement.id}/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403
