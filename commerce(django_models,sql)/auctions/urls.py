from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create"),
    path("listing/<str:title>/", views.listing_view, name="listing"),
    path("watchlist/<str:username>/", views.watchlist_view, name="watchlist"),
    path("categories", views.categories_view, name="categories"),
    path("categories/<str:category>/", views.category_view, name="category"),
]
