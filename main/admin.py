from django.contrib import admin

from .models import Property

class PropertyAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Property, PropertyAdmin)
