from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Registration

@login_required
def dashboard_redirect(request):
    """Checks the user role and sends them to the right dashboard."""
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
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