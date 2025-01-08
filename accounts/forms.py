from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    """Custom form to restrict max length for username and password."""
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(),
        help_text="20 characters or fewer. Letters, digits, and @/./+/-/_ only."
    )
    password1 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(),
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(),
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
