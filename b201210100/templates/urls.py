from django import views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("analyses/", views.analyses, name="analyses"),
    path("data/", views.data, name="data"),
]
