from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Event


class RegistrationForm(UserCreationForm):
    """Create a user registration form with required fields."""
    first_name = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

    class Meta:
        """Meta class to interact with models as well as provide the metadata to the form."""
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        # Function to set common attributes
        def set_common_attrs(field, placeholder):
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': placeholder})
            self.fields[field].label = ''

        # Set common attributes
        fields_attrs = {
            'username': 'User Name',
            'password1': 'Password',
            'password2': 'Confirm Password'
        }
        for field, placeholder in fields_attrs.items():
            set_common_attrs(field, placeholder)

        # Set help text
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']