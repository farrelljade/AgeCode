from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    """A user created community event."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', default='default.jpg')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.title
    
class EventAttendance(models.Model):
    """Model to track user attendance at events."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # Additional fields if needed, like registration date

    class Meta:
        unique_together = ('user', 'event')  # Prevents duplicate attendance records

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.user.username} is attending: {self.event.title}"
