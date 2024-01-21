from django.contrib import admin
from .models import Event, EventAttendance, Profile


admin.site.register(Event)
admin.site.register(EventAttendance)
admin.site.register(Profile)

