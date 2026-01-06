from django.shortcuts import render
from .forms import CustomerRegistrationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_status_valid():
            user = form.save(commit=False)
            user.role = 'CUSTOMER'  # Force the role to Customer
            user.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})