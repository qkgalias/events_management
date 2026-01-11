from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StyledAuthenticationForm, StyledUserCreationForm 
from django.contrib.auth import login, logout as auth_logout 
from django.contrib import messages 
from .models import Event, Registration
from django.utils import timezone
from django.urls import reverse

# 1. SIGNUP LOGIC
def signup(request):
    """Handles standalone signup requests and redirections."""
    if request.method == 'POST':
        # Server-side validation for Terms and Conditions checkbox
        if not request.POST.get('terms_check'):
            messages.error(request, "You must agree to the Terms of Service to create an account.")
            return redirect('homepage')

        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse('homepage') + '?signup_success=true')
    else:
        form = StyledUserCreationForm()
    return render(request, 'events/components/signup_form.html', {'signup_form': form})

# 2. REDIRECT LOGIC
@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('admin:index')
    return redirect('homepage')

# 3. HOMEPAGE VIEW
def homepage(request):
    """The public landing page showing all seminars."""
    request.session['detail_origin'] = 'home' 
    
    login_form = StyledAuthenticationForm()
    signup_form = StyledUserCreationForm()
    
    if request.method == 'POST':
        if 'username' in request.POST and 'email' not in request.POST:
            login_form = StyledAuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Successfully logged in as {user.username}")
                return redirect('homepage')
        elif 'email' in request.POST:
            # Server-side Terms check for modal-based signup
            if not request.POST.get('terms_check'):
                messages.error(request, "You must agree to the Terms of Service to register.")
                return redirect('homepage')

            signup_form = StyledUserCreationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                return redirect(reverse('homepage') + '?signup_success=true')
    
    events = Event.objects.all()
    registered_event_ids = []
    if request.user.is_authenticated:
        registered_event_ids = list(Registration.objects.filter(user=request.user).values_list('event_id', flat=True))
    
    return render(request, 'events/homepage.html', {
        'events': events,
        'registered_event_ids': registered_event_ids,
        'form': login_form, 
        'signup_form': signup_form,
    })

# 4. FULL SCHEDULE VIEW
def full_schedule(request):
    """View to display all upcoming seminars."""
    origin_param = request.GET.get('origin')
    if origin_param == 'dashboard':
        request.session['detail_origin'] = 'profile'
    else:
        request.session['detail_origin'] = 'schedule' 
    
    login_form = StyledAuthenticationForm()
    signup_form = StyledUserCreationForm()
    
    if request.method == 'POST':
        if 'username' in request.POST and 'email' not in request.POST:
            login_form = StyledAuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Successfully logged in as {user.username}")
                return redirect('full_schedule')
        elif 'email' in request.POST:
            # Server-side Terms check
            if not request.POST.get('terms_check'):
                messages.error(request, "You must agree to the Terms of Service to register.")
                return redirect('full_schedule')

            signup_form = StyledUserCreationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                return redirect(reverse('full_schedule') + '?signup_success=true')

    events = Event.objects.all().order_by('date', 'time')
    search_query = request.GET.get('search', '') 
    category_filter = request.GET.get('category')
    
    if search_query:
        events = events.filter(title__icontains=search_query) | events.filter(description__icontains=search_query)
    if category_filter:
        events = events.filter(category=category_filter)
    
    registered_event_ids = []
    if request.user.is_authenticated:
        registered_event_ids = list(Registration.objects.filter(user=request.user).values_list('event_id', flat=True))
    
    categories = Event.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'events/full_schedule.html', {
        'events': events,
        'categories': categories,
        'selected_category': category_filter,
        'search_query': search_query,
        'registered_event_ids': registered_event_ids,
        'form': login_form, 
        'signup_form': signup_form,
        'origin': request.session.get('detail_origin') 
    })
    
# 5. EVENT DETAILS VIEW
def event_detail(request, event_id):
    """Public detail view for specific seminars."""
    event = get_object_or_404(Event, id=event_id)
    request.session['last_event_detail'] = request.path 
    
    url_origin = request.GET.get('origin')
    if url_origin:
        origin = url_origin
        request.session['detail_origin'] = url_origin 
    else:
        origin = request.session.get('detail_origin', 'home')
    
    login_form = StyledAuthenticationForm()
    signup_form = StyledUserCreationForm()
    
    if request.method == 'POST':
        if 'username' in request.POST and 'email' not in request.POST:
            login_form = StyledAuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Successfully logged in as {user.username}")
                return redirect('event_detail', event_id=event.id)
        elif 'email' in request.POST:
            # Server-side Terms check
            if not request.POST.get('terms_check'):
                messages.error(request, "You must agree to the Terms of Service to register.")
                return redirect('event_detail', event_id=event.id)

            signup_form = StyledUserCreationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                return redirect(reverse('event_detail', kwargs={'event_id': event.id}) + '?signup_success=true')

    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(user=request.user, event=event).exists()
        
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'origin': origin,
        'form': login_form, 
        'signup_form': signup_form,
    })

# 6. JOIN EVENT 
@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration, created = Registration.objects.get_or_create(user=request.user, event=event)
    if created:
        messages.success(request, f'Successfully registered!', extra_tags='registration_success')
    else:
        messages.info(request, f'You are already registered for {event.title}.')
    return redirect('event_detail', event_id=event.id)

# 7. PROFILE DASHBOARD
@login_required
def profile_dashboard(request):
    """User profile dashboard with smart navigation to prevent back-button loops."""
    referer = request.META.get('HTTP_REFERER', '')
    profile_url = reverse('profile_dashboard')
    
    is_returning = request.GET.get('returning') == 'true'

    if not is_returning:
        if referer and profile_url not in referer:
            request.session['profile_return_url'] = referer
    
    if not request.session.get('profile_return_url'):
        request.session['profile_return_url'] = reverse('homepage')

    request.session['detail_origin'] = 'profile' 
    
    my_registrations = Registration.objects.filter(user=request.user).select_related('event')
    
    now = timezone.now()
    upcoming_count = my_registrations.filter(event__date__gte=now.date()).count()
    
    return render(request, 'events/profile_dashboard.html', {
        'my_registrations': my_registrations,
        'upcoming_count': upcoming_count
    })

# 8. CANCEL REGISTRATION 
@login_required
def cancel_event(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == "POST":
        registration.delete()
        messages.success(request, f'Registration cancelled.')
    return redirect('profile_dashboard')

# 9. LOGOUT VIEW 
def logout_user(request):
    """Logs out user and returns them to the previous page with a success message."""
    referer = request.META.get('HTTP_REFERER', reverse('homepage'))
    
    auth_logout(request)
    messages.success(request, "Successfully logged out. See you again!")

    # Redirect to homepage if logging out from the protected profile page
    if reverse('profile_dashboard') in referer:
        return redirect('homepage')
        
    return redirect(referer)