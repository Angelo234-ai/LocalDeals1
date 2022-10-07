import uuid
from django.db import models
from django.db.models.fields.related import OneToOneField
from django.contrib.auth.models import User
import datetime


# Create your models here.


class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE,
                         related_name="profile", blank=True, null=True, )
    username = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.ImageField(
        blank=True, null=True, upload_to="users/profiles-images", default="team/team1.jpg")
    created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    email = models.EmailField(max_length=254, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(max_length=500, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True)
    stared = models.BooleanField(default=False, null=True)
    trash = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.sender.username

    class Meta:
        ordering = ["is_read", "-created", ]
