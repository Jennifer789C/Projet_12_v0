from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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


class PersonnelAdmin(UserAdmin):
    add_form = CreationUserForm

    ordering = ("id", )
    list_display = ("id", "nom", "prenom", "email", "equipe")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations personnelles", {"fields": ("nom", "prenom", "tel", "port")}),
        ("Autorisations", {"fields": ("equipe", "is_active")}),
        ("Dates", {"fields": ("date_joined", "last_login")}),
        ("Autres", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password", "equipe"),
        }),
    )


admin.site.register(Personnel, PersonnelAdmin)
