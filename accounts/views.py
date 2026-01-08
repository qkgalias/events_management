from django.shortcuts import render, redirect 
from django.contrib import messages
from .forms import CustomerRegistrationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'CUSTOMER'  # Force the role to Customer
            user.save() # Save the user to the database
            messages.success(request, f'Account created for {user.username}! You can now login.')
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})