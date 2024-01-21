from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

# Signal to create or update the user profile whenever a user object is created or saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

class Event(models.Model):
    """A user created community event."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    event_capacity = models.IntegerField(default=0, verbose_name='Capacity')
    spots_remaining = models.IntegerField(default=0, verbose_name='Spots Remaining')
    image = models.ImageField(upload_to='event_images/', default='default.jpg')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if this is a new event.
            self.spots_remaining = self.event_capacity
        super().save(*args, **kwargs)

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
