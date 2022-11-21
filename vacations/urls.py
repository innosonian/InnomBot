from django.urls import path

from . import views

app_name = "restaurants"

urlpatterns = [
    path('', views.VacationAPI.as_view())
]