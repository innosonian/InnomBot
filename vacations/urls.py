from django.urls import path

from . import views

app_name = "vacations"

urlpatterns = [
    path('check', views.VacationCheckAPI.as_view()),
    path('', views.VacationCreateAPI.as_view())
]