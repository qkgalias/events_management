"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# ONLY import views here in the urls.py file
from events.views import dashboard_redirect
from accounts.views import signup # signup lives in accounts/views.py

urlpatterns = [
    
    path('admin/', admin.site.urls),
]

from django.contrib import admin
from django.urls import path, include
from accounts.views import signup # Import the new signup view

urlpatterns = [
    path('', dashboard_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/signup/', signup, name='signup'), # New signup route
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', include('events.urls')),
]