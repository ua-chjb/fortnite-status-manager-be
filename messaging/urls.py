from django.urls import path
from . import views

urlpatterns = [
    path("dm/", views.conversation_list, name="conversation-list"),
    path("dm/<int:pk>/", views.conversation_detail, name="conversation-detail"),
    path("dm/<int:conversation_pk>/messages/", views.message_list, name="message-list"),
    path("dm/<int:conversation_pk>/invites/", views.invite_list, name="invite-list"),
    path("invites/<int:pk>/accept/", views.invite_accept, name="invite-accept"),
    path("invites/<int:pk>/decline/", views.invite_decline, name="invite-decline")
]