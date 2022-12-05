from django.contrib import admin
from import_export.admin import ImportExportMixin

from vacations.models import Vacation, User, VacationType


# Register your models here.
@admin.register(Vacation)
class VacationAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'user', 'start_date', 'end_date', 'message', 'vacation_type', 'deleted_at', 'created_at']


@admin.register(User)
class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(VacationType)
class UserAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'name', 'weight']
