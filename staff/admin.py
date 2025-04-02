from django.contrib import admin

from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_approving_officer']
    list_editable = ['is_approving_officer']