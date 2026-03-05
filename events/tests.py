from datetime import date, time

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from .forms import StyledUserCreationForm
from .models import Event, Registration

User = get_user_model()


class SecurityRedirectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="StrongPass123!",
        )

    def test_logout_blocks_external_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout"), HTTP_REFERER="https://evil.test/redirect")
        self.assertRedirects(response, reverse("homepage"), fetch_redirect_response=False)

    def test_logout_is_post_only(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)

    def test_logout_redirects_profile_back_to_home(self):
        self.client.force_login(self.user)
        profile_url = reverse("profile_dashboard")
        response = self.client.post(reverse("logout"), HTTP_REFERER=f"http://testserver{profile_url}")
        self.assertRedirects(response, reverse("homepage"), fetch_redirect_response=False)

    def test_profile_dashboard_ignores_external_referer(self):
        self.client.force_login(self.user)
        self.client.get(reverse("profile_dashboard"), HTTP_REFERER="https://evil.test/phish")

        session = self.client.session
        self.assertEqual(session.get("profile_return_url"), reverse("homepage"))


class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="bob",
            email="bob@example.com",
            password="StrongPass123!",
        )
        self.event = Event.objects.create(
            title="Django Meetup",
            location="Online",
            date=date(2026, 5, 1),
            time=time(18, 0),
            capacity=100,
        )

    def test_registration_is_unique_per_user_event(self):
        Registration.objects.create(user=self.user, event=self.event)
        with self.assertRaises(IntegrityError):
            Registration.objects.create(user=self.user, event=self.event)

    def test_join_event_is_post_only(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("join_event", kwargs={"event_id": self.event.id}))
        self.assertEqual(response.status_code, 405)

    def test_cancel_event_is_post_only(self):
        self.client.force_login(self.user)
        registration = Registration.objects.create(user=self.user, event=self.event)
        response = self.client.get(reverse("cancel_event", kwargs={"registration_id": registration.id}))
        self.assertEqual(response.status_code, 405)


class SignupValidationTests(TestCase):
    def test_signup_form_uses_password_validators(self):
        weak_form = StyledUserCreationForm(
            data={
                "username": "weak_user",
                "email": "weak@example.com",
                "password1": "123",
                "password2": "123",
            }
        )
        self.assertFalse(weak_form.is_valid())

        strong_form = StyledUserCreationForm(
            data={
                "username": "strong_user",
                "email": "strong@example.com",
                "password1": "VeryStrongPass123!",
                "password2": "VeryStrongPass123!",
            }
        )
        self.assertTrue(strong_form.is_valid())
