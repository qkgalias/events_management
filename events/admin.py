from django.contrib import admin
from .models import Event, Registration, Speaker

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    # This makes speakers easy to manage in the sidebar
    list_display = ('name', 'role', 'company')
    search_fields = ('name', 'company')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('title', 'location')
    # It MUST be a tuple, so use comma for separation
    filter_horizontal = ('speakers',)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registration_date')
    list_filter = ('event', 'registration_date')
    
    admin.site.site_header = "TechHub Admin Management"
    admin.site.site_title = "TechHub Admin Portal"
    admin.site.index_title = "Welcome to the Event Manager Backend"