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
    # Reset origin tracking when on the main landing page
    request.session['detail_origin'] = 'dashboard' 
    
    events = Event.objects.all()
    registered_event_ids = []
    if request.user.is_authenticated:
        registered_event_ids = list(Registration.objects.filter(
            user=request.user
        ).values_list('event_id', flat=True))
    
    return render(request, 'events/customer_dashboard.html', {
        'events': events,
        'registered_event_ids': registered_event_ids
    })

def full_schedule(request):
    """View to display all upcoming seminars with search and category filtering."""
    # Track that the user is viewing the full schedule list
    request.session['detail_origin'] = 'schedule' 
    
    events = Event.objects.all().order_by('date', 'time')
    
    search_query = request.GET.get('search', '') 
    category_filter = request.GET.get('category')
    
    if search_query:
        events = events.filter(title__icontains=search_query) | events.filter(description__icontains=search_query)
        
    if category_filter:
        events = events.filter(category=category_filter)
    
    registered_event_ids = []
    if request.user.is_authenticated:
        registered_event_ids = list(Registration.objects.filter(
            user=request.user
        ).values_list('event_id', flat=True))
    
    categories = Event.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'events/full_schedule.html', {
        'events': events,
        'categories': categories,
        'selected_category': category_filter,
        'search_query': search_query,
        'registered_event_ids': registered_event_ids
    })
    
def event_detail(request, event_id):
    """Public detail view for specific seminars."""
    event = get_object_or_404(Event, id=event_id)
    
    # Save exact URL so Profile can return here if clicked
    request.session['last_event_detail'] = request.path 
    
    # Check origin for breadcrumbs (Dashboard vs Schedule)
    origin = request.session.get('detail_origin', 'dashboard')
    
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(user=request.user, event=event).exists()
        
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'origin': origin 
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
    """User profile dashboard with dynamic back-navigation logic."""
    referer = request.META.get('HTTP_REFERER', '')
    
    # 1. Logic to determine where the 'Back' button should point
    if 'event/' in referer and 'last_event_detail' in request.session:
        # User arrived while viewing a specific event detail page
        request.session['detail_origin'] = 'event_detail' 
    elif 'schedule/' in referer:
        # User arrived while browsing the full schedule list
        request.session['detail_origin'] = 'schedule' 
    else:
        # User arrived from the main dashboard
        request.session['detail_origin'] = 'dashboard' 
    
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