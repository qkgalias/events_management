from django.db import models
from django.conf import settings

# Make sure the word "Event" is spelled exactly like this
class Event(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Published')

    def __str__(self):
        return self.title

class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    registration_date = models.DateTimeField(auto_now_add=True)