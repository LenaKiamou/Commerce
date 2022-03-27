from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create"),
    path("listing/<str:listing_id>", views.listing_view, name="listing"),
    path("categories", views.categories_view, name='categories'),
    path("categories/<str:category_id>", views.category_view, name='category'),
    path("comment/<str:listing_id>", views.comment_view, name="comment"),
    path("createBid/<str:listing_id>", views.create_bid, name="create bid"),
    path("watchlist", views.my_watchlist, name="my_watchlist"),
    path("watchlist/<str:listing_id>", views.watchlist_view, name="watchlist"),
    path("closed/<str:listing_id>", views.closed, name="closed"),
]
