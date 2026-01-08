from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_dashboard, name='customer_dashboard'), # Public Homepage
    path('dashboard/redirect/', views.dashboard_redirect, name='dashboard_redirect'), # Logic Controller for post-login
    path('event/<int:event_id>/', views.event_detail, name='event_detail'), # Event Details
    path('join/<int:event_id>/', views.join_event, name='join_event'), # Registration (login required)
    path('profile/', views.profile_dashboard, name='profile_dashboard'), # User Profile Dashboard
    path('cancel/<int:registration_id>/', views.cancel_event, name='cancel_event'), # Cancel Registration
]