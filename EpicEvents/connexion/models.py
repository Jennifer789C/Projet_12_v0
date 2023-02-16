from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, Group
from django.db.models.signals import m2m_changed


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Veuillez saisir une adresse mail")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Un superuser doit avoir l'option 'is_staff' activé")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Un superuser doit avoir l'option 'is_superuser' activé")

        return self._create_user(email, password, **extra_fields)


class Personnel(AbstractUser):
    GESTION = "GESTION"
    VENTE = "VENTE"
    SUPPORT = "SUPPORT"

    CHOIX = (
        (GESTION, "Gestion"),
        (VENTE, "Vente"),
        (SUPPORT, "Support")
    )

    first_name = None
    last_name = None
    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=25)
    tel = models.CharField(max_length=20)
    port = models.CharField(max_length=20, blank=True, null=True)
    equipe = models.CharField(max_length=10, choices=CHOIX)
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.groups.clear()
        groupe_gestion = Group.objects.get(name="gestion")
        groupe_vente = Group.objects.get(name="vente")
        groupe_support = Group.objects.get(name="support")
        if self.equipe == self.GESTION:
            self.is_staff = True
            groupe_gestion.user_set.add(self)
        elif self.equipe == self.VENTE:
            self.is_staff = False
            self.groups.add(groupe_vente)
        elif self.equipe == self.SUPPORT:
            self.is_staff = False
            self.groups.add(groupe_support)
        super().save(*args, **kwargs)
