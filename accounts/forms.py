from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomerRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Includes base fields (username + passwords) and adds email
        fields = UserCreationForm.Meta.fields + ("email",)