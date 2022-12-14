from django.urls import path

from . import views
from config import cron

app_name = "vacations"

urlpatterns = [
    path('check', views.vacation_get),
    path('apply', views.vacation_apply),
    path('reminder', views.vacation_reminder),
    path('', views.vacation_create_form)
]