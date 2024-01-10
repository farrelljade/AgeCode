from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from .models import Event


def home(request):
    """The home page for AgeCode."""
    return render(request, 'agecode/home.html')

def user_login(request):
    """Login page for AgeCode. Check to see if looing in."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in.")
            return redirect('agecode:home')
        else:
            # Return an invalid login error message.
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('agecode:login')
    else:
        return render(request, 'agecode/login.html')
    
def user_logout(request):
    """Logout page."""
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('agecode:home')

def register_user(request):
    """User registration form."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate/log user in.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('agecode:home')
    else:
        form = RegistrationForm()
        return render(request, 'agecode/register.html', {'form':form})
    
    return render(request, 'agecode/register.html', {'form':form})

@login_required
def user_events(request):
    query = request.GET.get('query', '')  # Get the search query

    if query:
        events = Event.objects.filter(location__icontains=query)  # Filter events by location
        header_message = (f"Events in {query.capitalize()}")
    else:
        events = Event.objects.all()  # Get all events if no query
        header_message = "All events"

    return render(request, 'agecode/events.html', {'events': events, 'header_message': header_message})
