from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from .models import Personnel


class CreationUserForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ("email", "password", "equipe")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


"""
class ModifUserForm(UserChangeForm):
    def save(self, commit=True):
        user = super(ModifUserForm, self).save(commit=False)
        equipe = self.cleaned_data["equipe"]
        groupe_gestion = Group.objects.get(name="gestion")
        groupe_vente = Group.objects.get(name="vente")
        groupe_support = Group.objects.get(name="support")
        if equipe == "GESTION":
            Personnel.groups.through.objects.create(personnel=user, group=groupe_gestion)
        elif equipe == "VENTE":
            groupe_vente.user_set.add(user)
        elif equipe == "SUPPORT":
            groupe_support.user_set.add(user)

        if commit:
            user.save()
            groupe_gestion.save()
            groupe_vente.save()
            groupe_support.save()
        return user
"""


class PersonnelAdmin(UserAdmin):
    add_form = CreationUserForm
    # form = ModifUserForm

    ordering = ("id", )
    list_display = ("id", "nom", "prenom", "email", "equipe")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations personnelles", {"fields": ("nom", "prenom", "tel", "port")}),
        ("Autorisations", {"fields": ("is_active", "groups")}),
        ("Dates", {"fields": ("date_joined", "last_login")}),
        ("Autres", {"fields": ("is_staff", "is_superuser", "equipe", "user_permissions")})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password", "equipe"),
        }),
    )


admin.site.register(Personnel, PersonnelAdmin)
