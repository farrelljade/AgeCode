from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, EventForm
from .models import Event, EventAttendance


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
            messages.error(request, 'Invalid credentials.')
            return redirect('agecode:home')
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


def add_event(request):
    """User event creation page."""
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.organizer = request.user  # Set the organizer as the current user
                event.save()
                messages.success(request, "Event created successfully.")
                return redirect('agecode:home')
        else:
            form = EventForm()
        return render(request, 'agecode/add_event.html', {'form':form})
    else:
        messages.error(request, "You must be logged in to create an event!")
        return redirect('agecode:home')


def user_events(request):
    """User events page."""
    if request.user.is_authenticated:
        query = request.GET.get('query', '')  # Get the search query

        if query:
            events = Event.objects.filter(location__icontains=query)  # Filter events by location
            header_message = (f"Upcoming events in {query.capitalize()}")
        else:
            events = Event.objects.all()  # Get all events if no query
            header_message = "Upcoming events"

        return render(request, 'agecode/events.html', {'events':events, 'header_message':header_message})
    else:
        messages.error(request, "You must be logged in to view upcoming events!")
        return redirect('agecode:home')


def event_details(request, pk):
    """Events details page."""
    if request.user.is_authenticated:
        event_details = Event.objects.get(id=pk)
        return render(request, 'agecode/details.html', {'event_details':event_details})
    else:
        messages.error(request, "You must be logged in to view event details page!")
        return redirect('agecode:home')
    
def attend_event(request, event_id):
    """User event attendance record."""
    if request.user.is_authenticated:
        event = Event.objects.get(id=event_id)
        EventAttendance.objects.get_or_create(user=request.user, event=event)  # get_or_create ensures users cant register for the same event more than once.
        messages.success(request, "Congratulations. You are attending the event...")
        return redirect('agecode:view_profile')
    else:
        messages.error(request, "You must be a registered user to attend events...")
        return redirect('agecode:home')
    
def view_profile(request):
    """User profile page."""
    if request.user.is_authenticated:
        # Fetch events user is attending
        attending_events = EventAttendance.objects.filter(user=request.user).select_related('event')

        # Pass the events to the template
        return render(request, 'agecode/view_profile.html', {'attending_events':attending_events})
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect('agecode:home')