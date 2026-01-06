from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('my-events/', views.customer_dashboard, name='customer_dashboard'),
]