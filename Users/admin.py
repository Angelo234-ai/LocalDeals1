from django.contrib import admin
from django.contrib.admin.decorators import register
from django.db.models.deletion import PROTECT
from .models import Profile, Message


# Register your models here.
admin.site.register(Profile)
admin.site.register(Message)
