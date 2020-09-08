from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('create', views.create, name="create"),
    path('random', views.random_entry, name="random"),
    path('<str:title>/', views.entry, name="entry")
]


