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
    first_name = None
    last_name = None
    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=25)
    tel = models.CharField(max_length=20)
    port = models.CharField(max_length=20, blank=True, null=True)
    groups = models.ForeignKey(to='auth.group', null=True, on_delete=models.SET_NULL, related_name="user_set")
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        groupe_gestion = Group.objects.get(name="gestion")
        groupe_vente = Group.objects.get(name="vente")
        groupe_support = Group.objects.get(name="support")
        if self.groups == groupe_gestion:
            self.is_staff = True
            groupe_gestion.user_set.add(self)
        elif self.groups == groupe_vente:
            self.is_staff = False
            groupe_vente.user_set.add(self)
        elif self.groups == groupe_support:
            self.is_staff = False
            groupe_support.user_set.add(self)
        super().save(*args, **kwargs)
