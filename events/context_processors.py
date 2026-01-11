from .forms import StyledAuthenticationForm, StyledUserCreationForm

def auth_forms(request):
    """
    Provides the styled login and signup forms to every template.
    This ensures placeholders like 'Username' and 'Password' appear.
    """
    return {
        'form': StyledAuthenticationForm(), # Updated to use the styled version
        'signup_form': StyledUserCreationForm() # Updated to use the styled version
    }