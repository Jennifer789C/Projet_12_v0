from django.contrib import admin
from .models import Personnel


class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "prenom", "email")


admin.site.register(Personnel, PersonnelAdmin)
