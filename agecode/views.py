from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
            messages.success(request, "You are logged in.")
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
