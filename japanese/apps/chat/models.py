from django.db import models
from django.contrib.auth.models import Group, User


# Create your models here.
class ChatGroup(models.Model):
    """ extend Group model to add extra info"""
    name = models.OneToOneField(Group, blank=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, help_text="description of the group")
    mute_notifications = models.BooleanField(default=False, help_text="disable notification if true")
    icon = models.ImageField(help_text="Group icon", blank=True, upload_to="chartgroup")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.group

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('chat:room', args=[str(self.id)])
