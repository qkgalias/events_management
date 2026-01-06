from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Registration

@login_required
def dashboard_redirect(request):
    """Checks the user role and sends them to the right dashboard."""
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    else:
        return redirect('customer_dashboard')

@login_required
def admin_dashboard(request):
    events = Event.objects.all()
    stats = {
        'total_events': events.count(),
        'total_registrations': Registration.objects.count(),
    }
    return render(request, 'events/admin_dashboard.html', {'events': events, 'stats': stats})

@login_required
def customer_dashboard(request):
    events = Event.objects.all() 
    my_events = Registration.objects.filter(user=request.user)
    return render(request, 'events/customer_dashboard.html', {'events': events, 'my_events': my_events})

@login_required
def join_event(request, event_id):
    """Processes the registration when a customer clicks 'Register'"""
    event = get_object_or_404(Event, id=event_id)
    # This checks if the user is already registered; if not, it creates the record
    Registration.objects.get_or_create(user=request.user, event=event)
    return redirect('customer_dashboard')