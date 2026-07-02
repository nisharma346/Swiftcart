from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm
from .models import CustomUser

# Create your views here.

def home(request):
    """
    Home page view
    """
    context = {
        'page_title': 'Home'
    }
    return render(request, 'swiftcart/home.html', context)


@require_http_methods(["GET", "POST"])
def register(request):
    """
    User registration view
    GET: Display the registration form
    POST: Process the registration form
    """
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                'Registration successful! Please log in with your email and password.'
            )
            return redirect('login')  # Redirect to login page after successful registration
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Register'
    }
    return render(request, 'swiftcart/register.html', context)


@require_http_methods(["GET", "POST"])
def user_login(request):
    """
    User login view
    GET: Display the login form
    POST: Process the login form
    """
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if already logged in
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Get user by email
            user = CustomUser.objects.get(email=email)
            # Authenticate with username (since username is set to email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.full_name}!')
                # Redirect to next page or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid email or password.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
    
    context = {
        'page_title': 'Login'
    }
    return render(request, 'swiftcart/login.html', context)


@login_required(login_url='login')
def user_logout(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
