from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    epic_account_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    epic_display_name = models.CharField(max_length=100, blank=True)
    epic_access_token = models.TextField(blank=True)
    epic_refresh_token = models.TextField(blank=True)
    epic_token_expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.epic_display_name or self.username
    

class Friendship(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship_reverse")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "friend")

    def __str__(self):
        return f"{self.user} -> {self.friend}"