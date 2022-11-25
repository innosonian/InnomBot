from django.contrib import admin

from vacations.models import Vacation, User


# Register your models here.
@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'start_date', 'end_date', 'message', 'deleted_at', 'created_at']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
