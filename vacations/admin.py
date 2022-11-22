from django.contrib import admin

from vacations.models import Vacation


# Register your models here.
@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'date', 'message', 'deleted_at', 'created_at']