from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Event


class RegistrationForm(UserCreationForm):
    """Create a user registration form with required fields."""
    image = forms.ImageField(required=False)  # Add an image field to the form (make it optional)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'image')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }
        labels = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'User Name'})
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Now we handle the image separately
            profile = user.profile  # This assumes you have created the profile in the signal
            profile.image = self.cleaned_data.get('image')
            profile.save()
        return user

class EventForm(forms.ModelForm):
    """Create an event registration form. User has to be logged in."""
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'event_capacity', 'spots_remaining', 'location', 'image',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'event_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'spots_remaining': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Location'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '',
            'description': '',
            'date': '',
            'location': '',
        }