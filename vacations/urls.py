from django.urls import path

from . import views

app_name = "vacations"

urlpatterns = [
    path('check', views.vacation_get),
    path('apply', views.vacation_apply),
    path('', views.vacation_create_form)
]