from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    """A user created community event."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.title
