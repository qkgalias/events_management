from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('', views.homepage, name='homepage'), # Public Homepage
    
    # Authentication Routes
    path('login/', auth_views.LoginView.as_view(template_name='events/components/login_form.html'), name='login'), # Modal Login Controller
    path('signup/', views.signup, name='signup'), # New User Registration
    path('logout/', views.logout_user, name='logout'), 
    path('dashboard/redirect/', views.dashboard_redirect, name='dashboard_redirect'), # Logic Controller for post-login

    # Password Reset Routes
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='events/resetpass_form.html',
        html_email_template_name='events/password_reset_email.html',
        email_template_name='events/password_reset_email.txt',
        subject_template_name='events/password_reset_subject.txt'
    ), name='password_reset'), # Submit Email for Reset
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='events/resetpass_done.html'), name='password_reset_done'), # Email Sent Confirmation
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='events/resetpass_confirm.html'), name='password_reset_confirm'), # New Password Input
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='events/resetpass_complete.html'), name='password_reset_complete'), # Reset Success Confirmation

    # Event Routes
    path('schedule/', views.full_schedule, name='full_schedule'), # Full Schedule View
    path('event/<int:event_id>/', views.event_detail, name='event_detail'), # Event Details
    path('join/<int:event_id>/', views.join_event, name='join_event'), # Registration (login required)
    path('profile/', views.profile_dashboard, name='profile_dashboard'), # User Profile Dashboard
    path('cancel/<int:registration_id>/', views.cancel_event, name='cancel_event'), # Cancel Registration
]