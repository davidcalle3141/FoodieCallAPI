# Register your models here.
from django.contrib import admin

from .models import Event, Image

admin.site.register(Event)
admin.site.register(Image)