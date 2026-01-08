from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Event, Registration

@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('admin:index')
    return redirect('customer_dashboard')

def customer_dashboard(request):
    """The public landing page showing all seminars."""
    events = Event.objects.all()
    # Create a list of event IDs the user is registered for
    registered_event_ids = []
    if request.user.is_authenticated:
        registered_event_ids = list(Registration.objects.filter(
            user=request.user
        ).values_list('event_id', flat=True))
    
    return render(request, 'events/customer_dashboard.html', {
        'events': events,
        'registered_event_ids': registered_event_ids # Pass this list to the template
    })

def event_detail(request, event_id):
    """Public detail view for specific seminars."""
    event = get_object_or_404(Event, id=event_id)
    # Check if this specific user is registered for this specific event
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(user=request.user, event=event).exists()
        
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered 
    })

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registration, created = Registration.objects.get_or_create(user=request.user, event=event)
    
    if created:
        messages.success(request, f'Successfully registered!', extra_tags='registration_success')
    else:
        messages.info(request, f'You are already registered for {event.title}.')
        
    return redirect('event_detail', event_id=event.id)

@login_required
def profile_dashboard(request):
    my_registrations = Registration.objects.filter(user=request.user).select_related('event')
    return render(request, 'events/profile_dashboard.html', {
        'my_registrations': my_registrations
    })

@login_required
def cancel_event(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == "POST":
        registration.delete()
        messages.success(request, f'Registration cancelled.')
    return redirect('profile_dashboard')