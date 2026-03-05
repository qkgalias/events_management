from urllib.parse import urlsplit

from django.contrib import messages
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import StyledAuthenticationForm, StyledUserCreationForm
from .models import Event, Registration

VALID_ORIGINS = {"home", "schedule", "profile"}


def _normalize_origin(origin_value, default="home"):
    return origin_value if origin_value in VALID_ORIGINS else default


def _safe_local_url(request, candidate, fallback):
    if not candidate:
        return fallback

    allowed_hosts = {request.get_host()}
    if not url_has_allowed_host_and_scheme(
        candidate,
        allowed_hosts=allowed_hosts,
        require_https=request.is_secure(),
    ):
        return fallback

    parsed = urlsplit(candidate)
    path = parsed.path or "/"
    if parsed.query:
        return f"{path}?{parsed.query}"
    return path


def _handle_modal_auth(request, success_redirect_url, signup_success_url):
    login_form = StyledAuthenticationForm(request=request)
    signup_form = StyledUserCreationForm()

    if request.method != "POST":
        return login_form, signup_form, None

    is_login = "username" in request.POST and "email" not in request.POST
    is_signup = "email" in request.POST

    if is_login:
        login_form = StyledAuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f"Successfully logged in as {user.username}")
            return login_form, signup_form, redirect(success_redirect_url)

    if is_signup:
        if not request.POST.get("terms_check"):
            messages.error(request, "You must agree to the Terms of Service to register.")
            return login_form, signup_form, redirect(success_redirect_url)

        signup_form = StyledUserCreationForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return login_form, signup_form, redirect(signup_success_url)

    return login_form, signup_form, None


# 1. SIGNUP LOGIC
def signup(request):
    """Handles standalone signup requests and redirections."""
    if request.method == "POST":
        if not request.POST.get("terms_check"):
            messages.error(request, "You must agree to the Terms of Service to create an account.")
            return redirect("homepage")

        form = StyledUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("homepage") + "?signup_success=true")
    else:
        form = StyledUserCreationForm()

    return render(request, "events/components/signup_form.html", {"signup_form": form})


# 2. REDIRECT LOGIC
@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect("admin:index")
    return redirect("homepage")


# 3. HOMEPAGE VIEW
def homepage(request):
    """The public landing page showing all seminars."""
    request.session["detail_origin"] = "home"

    login_form, signup_form, auth_response = _handle_modal_auth(
        request=request,
        success_redirect_url=reverse("homepage"),
        signup_success_url=reverse("homepage") + "?signup_success=true",
    )
    if auth_response:
        return auth_response

    events = Event.objects.all()
    registered_event_ids = []
    if request.user.is_authenticated:
        registered_event_ids = list(
            Registration.objects.filter(user=request.user).values_list("event_id", flat=True)
        )

    return render(
        request,
        "events/homepage.html",
        {
            "events": events,
            "registered_event_ids": registered_event_ids,
            "form": login_form,
            "signup_form": signup_form,
        },
    )


# 4. FULL SCHEDULE VIEW
def full_schedule(request):
    """View to display all upcoming seminars."""
    origin_param = request.GET.get("origin")
    request.session["detail_origin"] = "profile" if origin_param == "dashboard" else "schedule"

    login_form, signup_form, auth_response = _handle_modal_auth(
        request=request,
        success_redirect_url=reverse("full_schedule"),
        signup_success_url=reverse("full_schedule") + "?signup_success=true",
    )
    if auth_response:
        return auth_response

    events = Event.objects.all().order_by("date", "time")
    search_query = request.GET.get("search", "")
    category_filter = request.GET.get("category")

    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        ).distinct()
    if category_filter:
        events = events.filter(category=category_filter)

    registered_event_ids = []
    if request.user.is_authenticated:
        registered_event_ids = list(
            Registration.objects.filter(user=request.user).values_list("event_id", flat=True)
        )

    categories = Event.objects.values_list("category", flat=True).distinct()

    return render(
        request,
        "events/full_schedule.html",
        {
            "events": events,
            "categories": categories,
            "selected_category": category_filter,
            "search_query": search_query,
            "registered_event_ids": registered_event_ids,
            "form": login_form,
            "signup_form": signup_form,
            "origin": request.session.get("detail_origin"),
        },
    )


# 5. EVENT DETAILS VIEW
def event_detail(request, event_id):
    """Public detail view for specific seminars."""
    event = get_object_or_404(Event, id=event_id)
    request.session["last_event_detail"] = request.path

    url_origin = request.GET.get("origin")
    if url_origin:
        origin = _normalize_origin(url_origin)
        request.session["detail_origin"] = origin
    else:
        origin = _normalize_origin(request.session.get("detail_origin", "home"))

    login_form, signup_form, auth_response = _handle_modal_auth(
        request=request,
        success_redirect_url=reverse("event_detail", kwargs={"event_id": event.id}),
        signup_success_url=reverse("event_detail", kwargs={"event_id": event.id}) + "?signup_success=true",
    )
    if auth_response:
        return auth_response

    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(user=request.user, event=event).exists()

    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,
            "is_registered": is_registered,
            "origin": origin,
            "form": login_form,
            "signup_form": signup_form,
        },
    )


# 6. JOIN EVENT
@login_required
@require_POST
def join_event(request, event_id):
    """Handles event registration and triggers the success modal."""
    event = get_object_or_404(Event, id=event_id)

    try:
        _, created = Registration.objects.get_or_create(user=request.user, event=event)
    except IntegrityError:
        created = False

    origin = _normalize_origin(request.session.get("detail_origin", "home"))

    if created:
        messages.success(request, "Successfully registered!", extra_tags="registration_success")
    else:
        messages.info(request, f"You are already registered for {event.title}.")

    return redirect(reverse("event_detail", kwargs={"event_id": event.id}) + f"?origin={origin}")


# 7. PROFILE DASHBOARD
@login_required
def profile_dashboard(request):
    """User profile dashboard with smart navigation to prevent back-button loops."""
    referer = request.META.get("HTTP_REFERER", "")
    profile_url = reverse("profile_dashboard")

    is_returning = request.GET.get("returning") == "true"

    if not is_returning:
        safe_referer = _safe_local_url(request, referer, "")
        if safe_referer and not safe_referer.startswith(profile_url):
            request.session["profile_return_url"] = safe_referer

    if not request.session.get("profile_return_url"):
        request.session["profile_return_url"] = reverse("homepage")

    request.session["detail_origin"] = "profile"

    my_registrations = Registration.objects.filter(user=request.user).select_related("event")

    now = timezone.now()
    upcoming_count = my_registrations.filter(event__date__gte=now.date()).count()

    return render(
        request,
        "events/profile_dashboard.html",
        {
            "my_registrations": my_registrations,
            "upcoming_count": upcoming_count,
        },
    )


# 8. CANCEL REGISTRATION
@login_required
@require_POST
def cancel_event(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    registration.delete()
    messages.success(request, "Registration cancelled.")
    return redirect("profile_dashboard")


# 9. LOGOUT VIEW
@require_POST
def logout_user(request):
    """Logs out user and returns them to a safe previous page."""
    referer = request.META.get("HTTP_REFERER")
    homepage_url = reverse("homepage")
    profile_url = reverse("profile_dashboard")
    safe_referer = _safe_local_url(request, referer, homepage_url)

    auth_logout(request)
    messages.success(request, "Successfully logged out. See you again!")

    if safe_referer.startswith(profile_url):
        return redirect(homepage_url)

    return redirect(safe_referer)
