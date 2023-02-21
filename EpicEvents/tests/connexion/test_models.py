from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client
import pytest

Personnel = get_user_model()
client = Client()


@pytest.mark.django_db
def test_creation_gestionnaire():
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
    assert gestionnaire.is_superuser is False
    assert gestionnaire.has_perms(permissions) is True
    assert gestionnaire.has_perm("api.create_client") is False


@pytest.mark.django_db
def test_creation_vendeur():
    vendeur = Personnel.objects.create_user(email="test@mail.fr", password="test")
    groupe_vente = Group.objects.get(name="vente")
    groupe_vente.user_set.add(vendeur)
    vendeur.save()
    permissions = ["api.add_client", "api.view_client", "api.change_client",
                   "api.add_contrat", "api.view_contrat", "api.change_contrat",
                   "api.add_evenement", "api.view_evenement", "api.change_evenement"]
    assert vendeur.email == "test@mail.fr"
    assert vendeur.is_staff is False
    assert vendeur.has_perms(permissions) is True
    assert vendeur.has_module_perms("connexion") is False
    assert vendeur.has_perm("api.delete_client") is False


@pytest.mark.django_db
def test_creation_technicien():
    technicien = Personnel.objects.create_user(email="test@mail.fr", password="test")
    groupe_support = Group.objects.get(name="support")
    groupe_support.user_set.add(technicien)
    technicien.save()
    permissions = ["api.view_client", "api.view_evenement", "api.change_evenement"]
    assert technicien.email == "test@mail.fr"
    assert technicien.is_staff is False
    assert technicien.has_perms(permissions) is True
    assert technicien.has_module_perms("connexion") is False
    assert technicien.has_perm("api.change_client") is False
    assert technicien.has_perm("api.add_contrat") is False


@pytest.mark.django_db
def test_creation_superuser():
    admin = Personnel.objects.create_superuser(email="test@mail.fr", password="test")
    permissions = ["connexion.add_personnel", "connexion.view_personnel", "connexion.change_personnel", "connexion.delete_personnel",
                   "api.add_client", "api.view_client", "api.change_client", "api.delete_client",
                   "api.add_contrat", "api.view_contrat", "api.change_contrat", "api.delete_contrat",
                   "api.add_evenement", "api.view_evenement", "api.change_evenement", "api.delete_evenement"]
    assert admin.email == "test@mail.fr"
    assert admin.is_staff is True
    assert admin.is_superuser is True
    assert admin.has_perms(permissions) is True


@pytest.mark.django_db
def test_modification_utilisateur():
    utilisateur = Personnel.objects.create_user(email="test@mail.fr", password="test")
    groupe_vente = Group.objects.get(name="vente")
    utilisateur.groups = groupe_vente
    utilisateur.save()
    assert utilisateur.is_staff is False

    groupe_gestion = Group.objects.get(name="gestion")
    utilisateur.groups = groupe_gestion
    utilisateur.save()
    assert utilisateur.is_staff is True
