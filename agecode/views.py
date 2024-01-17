from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, EventForm
from .models import Event, EventAttendance


def home(request):
    """The home page for AgeCode."""
    events = Event.objects.all()
    return render(request, 'agecode/home.html', {'events':events})


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
            form = EventForm(request.POST, request.FILES)
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
        # Get IDs of events the user is attending
        attending_event_ids = set(EventAttendance.objects.filter(user=request.user).values_list('event_id', flat=True))
        context = {
            'events': events,
            'header_message': header_message,
            'attending_event_ids': attending_event_ids,
        }
        return render(request, 'agecode/events.html', context)
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
        if event.spots_remaining > 0:
            # Check if the user has already registered.
            attendance, created = EventAttendance.objects.get_or_create(user=request.user, event=event)
            if created:
                event.spots_remaining -= 1
                event.save()
                messages.success(request, "Congratulations. You are attending the event...")
            else:
                messages.info(request, "You have already registered for this event.")
        else:
            messages.error(request, "Sorry, this event has reached its capacity.")
        
        return redirect('agecode:events')
    else:
        messages.error(request, "You must be a registered user to attend events...")
        return redirect('agecode:home')
    

def cancel_event(request, event_id):
    """Cancelling an event."""
    if request.user.is_authenticated:
        event = Event.objects.get(id=event_id)
        attendance_record = EventAttendance.objects.filter(user=request.user, event=event)
        if attendance_record.exists():
            attendance_record.delete()
            messages.success(request, "You have cancelled your attendance.")
            return redirect('agecode:events')
        else:
            messages.error(request, "You are not registered for this event.")
        return redirect('agecode:details', pk=event_id)
    else:
        messages.error(request, "You must be logged in to cancel an event.")
        return redirect('agecode:home')
    

def view_profile(request):
    """User profile page."""
    if request.user.is_authenticated:
        # Fetch the amount of events the user is attending
        event_count = EventAttendance.objects.filter(user=request.user).count()
        # Fetch the events user is attending
        attending_events = EventAttendance.objects.filter(user=request.user).select_related('event')
        context = {
            'attending_events': attending_events,
            'event_count': event_count
        }
        return render(request, 'agecode/view_profile.html', context)
    else:
        messages.error(request, "You must be logged in to view this page!")
        return redirect('agecode:home')