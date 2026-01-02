from django.db import models
from django.conf import settings

class Conversation(models.Model):

    name = models.CharField(max_length=100, blank=True)
    is_group = models.BooleanField(default=False)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_group:
            return self.name or f"Group {self.id}"
        return f"DM {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"
    
class GameInvite(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "pending"
        ACCEPTED = "accepted", "accepted"
        DECLINED = "declined", "declined"

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="invites"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_invites"
    )
    content = models.TextField(
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invite from {self.sender} - {self.status}"