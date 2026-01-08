from django.shortcuts import render, redirect 
from django.contrib import messages
from .forms import CustomerRegistrationForm

def signup(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'CUSTOMER'  
            user.save() 
            
            messages.success(request, f'Account created for {user.username}!')
            
            # Logic: Redirect based on Staff status
            if user.is_staff:
                return redirect('admin:index') # Sends to the Django Admin
            return redirect('login') # Sends customers to login first
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})