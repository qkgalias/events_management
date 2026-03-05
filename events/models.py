from django.db import models
from django.conf import settings

# 1. SPEAKER MODEL
# Defined first so Event can reference it in a ManyToManyField
class Speaker(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100) # e.g., "Head of AI"
    company = models.CharField(max_length=100) # e.g., "Google Cloud"
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='speakers/', blank=True, null=True)

    def __str__(self):
        return self.name

# 2. EVENT MODEL
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('Cybersecurity', 'Cybersecurity'),
        ('IT Seminar', 'IT Seminar'),
        ('Web Development', 'Web Development'),
        ('Data Science', 'Data Science'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='IT Seminar')
    banner_image = models.ImageField(upload_to='event_banners/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    date = models.DateField() # Stores YYYY-MM-DD
    time = models.TimeField() # Stores HH:MM:SS
    capacity = models.PositiveIntegerField()
    # Many-to-Many allows one speaker to attend many seminars
    speakers = models.ManyToManyField(Speaker, related_name='events', blank=True)
    status = models.CharField(max_length=20, default='Published')

    def __str__(self):
        return self.title

# 3. REGISTRATION MODEL
class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # related_name='participants' enables the counting logic in templates
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "event"], name="unique_user_event_registration")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
