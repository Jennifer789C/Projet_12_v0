from django.contrib.auth.models import Group
import pytest


@pytest.mark.django_db
def test_creation_gestionnaire(Personnel):
    gestionnaire = Personnel.objects.create_user(email="test@mail.fr", password="test")
    groupe_gestion = Group.objects.get(name="gestion")
    groupe_gestion.user_set.add(gestionnaire)
    gestionnaire.save()
    permissions = ["connexion.add_personnel", "connexion.view_personnel", "connexion.change_personnel", "connexion.delete_personnel",
                   "api.view_client", "api.change_client",
                   "api.view_contrat", "api.change_contrat",
                   "api.view_evenement", "api.change_evenement"]
    assert gestionnaire.email == "test@mail.fr"
    assert gestionnaire.is_staff is True
    assert gestionnaire.has_perms(permissions) is True
    assert gestionnaire.has_perm("api.create_client") is False


@pytest.mark.django_db
def test_creation_vendeur(Personnel):
    pass


@pytest.mark.django_db
def test_creation_technicien(Personnel):
    pass


@pytest.mark.django_db
def test_creation_superuser(Personnel):
    pass


@pytest.mark.django_db
def test_modification_utilisateur(Personnel):
    pass
