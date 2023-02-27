import pytest


@pytest.mark.django_db
def test_list_contrat_sans_authentification(apiclient, contrat):
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/")
    assert reponse.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize("token", ["token_access_gestionnaire",
                                   "token_access_technicien"])
def test_list_contrat_sans_permission(apiclient, contrat, token, request):
    token = request.getfixturevalue(token)
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/", HTTP_AUTHORIZATION="Bearer "+token)
    assert reponse.status_code == 403


@pytest.mark.django_db
def test_list_contrat(apiclient, contrat, token_access_vendeur):
    reponse = apiclient.get(f"/client/{contrat.client.id}/contrat/",
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
