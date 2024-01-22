from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .forms import RegistrationForm, EventForm, ProfileForm
from .models import Event, EventAttendance, Profile
from django.contrib.auth.models import User


def home(request):
    """The home page for AgeCode."""
    events = Event.objects.all()
    if request.user.is_authenticated:
        user_name = request.user.first_name
        if user_name:
            user_name = user_name[0].upper() + user_name[1:]
    else:
        user_name = ''
    return render(request, 'agecode/home.html', {'events':events, 'user_name':user_name})


def user_login(request):
    """Login page for AgeCode. Check to see if logged in."""
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
        form = RegistrationForm(request.POST, request.FILES)
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


def event_details(request, event_id):
    """Events details page."""
    if request.user.is_authenticated:
        # Show the specific event using the primary key
        event = get_object_or_404(Event, id=event_id)

        # Get IDs of events the user is attending
        attending_event_ids = set(EventAttendance.objects.filter(user=request.user).values_list('event_id', flat=True))
        # Count the total number of attendees for the event
        total_attendees = EventAttendance.objects.filter(event=event).count()
        # Get the name of the attendees
        attendees = User.objects.filter(eventattendance__event=event)

        context = {
            'event': event,
            'attending_event_ids': attending_event_ids,
            'total_attendees': total_attendees,
            'attendees': attendees,
        }
        return render(request, 'agecode/details.html', context)
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
            event.spots_remaining += 1
            event.save()
            messages.success(request, "You have cancelled your attendance.")
            return redirect('agecode:events')
        else:
            messages.error(request, "You are not registered for this event.")
        return redirect('agecode:details', pk=event_id)
    else:
        messages.error(request, "You must be logged in to cancel an event.")
        return redirect('agecode:home')
    

def edit_event(request, event_id):
    """User created events edit page."""
    if request.user.is_authenticated:
        # Show events created by specific user
        user_event = get_object_or_404(Event, id=event_id, organizer=request.user)

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request.
        form = EventForm(request.POST, request.FILES, instance=user_event)
        if form.is_valid():
            form.save()
            messages.success(request, "Your event has been updated...")
            return redirect('agecode:view_profile', user_id=request.user.id)
    else:
        # This else corresponds to if the request is not POST, meaning it is a GET request
        form = EventForm(instance=user_event)

    # Return outside of the conditional statement ensures that 'form' is always defined
    return render(request, 'agecode/edit_event.html', {'form': form})


@login_required
def edit_profile(request, pk):
    """User profile edit page."""
    profile_user = get_object_or_404(Profile, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully...")
            return redirect('agecode:view_profile', user_id=request.user.id)
    else:
        form = ProfileForm(instance=profile_user)

    return render(request, 'agecode/edit_profile.html', {'form': form})


@login_required
def delete_event(request, event_id):
    """User created events delete page."""
    user_event = get_object_or_404(Event, id=event_id, organizer=request.user)
    user_event.delete()
    messages.success(request, "Event deleted successfully...")
    return redirect('agecode:view_profile', user_id=request.user.id)
 

@login_required
def view_profile(request, user_id):
    """User profile page."""
    user = get_object_or_404(User, pk=user_id)

    # Show the amount of events the specified user is attending
    event_count = EventAttendance.objects.filter(user=user).count()

    # Show the events the specified user is attending with the count of attendees for each event
    attending_events = EventAttendance.objects.filter(user=user).select_related('event').annotate(total_attendees=Count('event__eventattendance'))

    # Show events created by the specified user with the count of attendees for each event
    created_events = Event.objects.filter(organizer=user).annotate(total_attendees=Count('eventattendance'))

    context = {
        'profile_user': user,  # Pass the user object to the template
        'attending_events': attending_events,
        'event_count': event_count,
        'created_events': created_events,
    }
    return render(request, 'agecode/view_profile.html', context)