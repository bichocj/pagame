from django.contrib import admin
from core.models import Person, AfpOnp, Company


class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "dni", "sex")
    ordering = ["name"]


admin.site.register(Person, PersonAdmin)
admin.site.register(AfpOnp)
admin.site.register(Company)
