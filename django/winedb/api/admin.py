from django.contrib import admin

from api.models import Wine

READONLY_FIELDS = []
LIST_HIDDEN_FIELDS = []

def column_lister(model):
    """ Creates a new ModelAdmin that always lists the models in a table fashion. """

    class ListAdmin(admin.ModelAdmin):
        readonly_fields = [
            f.name for f in model._meta.fields if f.name in READONLY_FIELDS
        ]
        list_display = [
            f.name for f in model._meta.fields if f.name not in LIST_HIDDEN_FIELDS
        ]

    return ListAdmin


# Register your models here.

admin.site.register(Wine, column_lister(Wine))
