from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Personnel


class CreationUserForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ("email", "password", "groups")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class PersonnelAdmin(UserAdmin):
    add_form = CreationUserForm

    ordering = ("id", )
    list_display = ("id", "nom", "prenom", "email", "groups")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations personnelles", {"fields": ("nom", "prenom", "tel", "port")}),
        ("Autorisations", {"fields": ("is_active", "groups")}),
        ("Dates", {"fields": ("date_joined", "last_login")})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password", "groups"),
        }),
    )
    filter_horizontal = ()


admin.site.register(Personnel, PersonnelAdmin)
