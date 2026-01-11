from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"

    # Overriding the default email field to make it unique and required
    email = models.EmailField(unique=True, blank=False, null=False)

    role = models.CharField(
        max_length=10, 
        choices=Role.choices, 
        default=Role.CUSTOMER
    )