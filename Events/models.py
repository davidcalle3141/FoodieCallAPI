from django.conf import settings
from django.db import models


class Event(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    event_name = models.CharField(max_length=50, default=date_created)
    is_active = models.BooleanField(default=True)
    has_happened = models.BooleanField(default=False)
    date_of_event = models.CharField(max_length=20, default="Today")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)


class Attendee(models.Model):
    event = models.ForeignKey(Event, related_name="attendees",
                              on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_going = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user')


class Image(models.Model):
    event = models.ForeignKey(Event, related_name="images",
                              on_delete=models.CASCADE)
    image = models.CharField(max_length=500)

    def __str__(self):
        return self.image


class Vote(models.Model):
    image = models.ForeignKey(Image, related_name="votes",
                              on_delete=models.CASCADE)
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE)
    voted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', "voted_by")
