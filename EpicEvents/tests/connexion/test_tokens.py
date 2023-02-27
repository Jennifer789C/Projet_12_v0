import pytest
from django.contrib.auth.models import Group


@pytest.mark.django_db
def test_obtention_tokens(apiclient, gestionnaire):
    reponse = apiclient.post("/login/",
                             data={"email": gestionnaire.email,
                                   "password": "test"},
                             )
    print(reponse.data["access"])


@pytest.mark.django_db
def test_permissions_gestionnaire(apiclient, gestionnaire):
    groupe_gestion = Group.objects.get(name="gestion")
    if gestionnaire.groups == groupe_gestion:
        print("l'user est bien dans le groupe gestion")
    else:
        print("erreur de groupe")
