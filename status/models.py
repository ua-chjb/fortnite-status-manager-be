from django.db import models
from django.conf import settings

class UserStatus(models.Model):

    class Availability(models.TextChoices):
        DO_NOT_DISTURB = "dnd", "do not disturb"
        COULD_BE_DOWN = "cbd", "could be down"
        READY_TO_PLAY = "rtp", "ready to play"

    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="status"
    )

    availability = models.CharField(
        max_length=3,
        choices=Availability.choices,
        default=Availability.DO_NOT_DISTURB
    )

    status_text = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.get_availability_display()}"