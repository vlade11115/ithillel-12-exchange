from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("current_rates/", views.current_rates, name="current_rates"),
]
