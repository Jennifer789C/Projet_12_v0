import pytest


@pytest.mark.django_db
def test_list_client(apiclient):
    reponse = apiclient.get("/client/")
    assert reponse.status_code == 200


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
    data = reponse.data
    assert reponse.status_code == 201
    assert data["societe"] == societe

