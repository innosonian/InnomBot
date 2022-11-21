from django.urls import path

from . import views

app_name = "vacations"

urlpatterns = [
    path('', views.VacationAPI.as_view())
]