from django.urls import path
from . import views
urlpatterns = [
    path("me/", views.me, name="me"),
    path("friends/", views.friend_list, name="friend-list"),
    path("friends/<int:pk>/", views.friend_detail, name="friend-detail"),
    path("home-feed/", views.home_feed, name="home-feed"),
    path("delete-account", views.delete_account, name="delete-account")
]