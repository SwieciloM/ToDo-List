from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import CustomUserCreationForm

VALID_USERNAME = "validUsername"
VALID_PASSWORD = "StrongPass123!"
MAX_LONG_USERNAME = "maxLengthUsername123"  # 20 characters
MAX_LONG_PASSWORD = "10charText" * 10  # 100 characters
TOO_LONG_USERNAME = "tooLongUsername123456"  # 21 characters
TOO_SHORT_PASSWORD = "shortPa"  # 7 characters
TOO_LONG_PASSWORD = "10charText" * 10 + "a"  # 101 characters


class TestCustomUserCreationForm(TestCase):
    def test_valid_form_data(self):
        """Form is valid with correct username and password."""
        form_data = {"username": VALID_USERNAME, "password1": VALID_PASSWORD, "password2": VALID_PASSWORD}
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_data_with_max_length(self):
        """Form is valid with maximum allowed username and password length."""
        form_data = {"username": MAX_LONG_USERNAME, "password1": MAX_LONG_PASSWORD, "password2": MAX_LONG_PASSWORD}
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_username_too_long(self):
        """Form is invalid if username exceeds maximum length."""
        form_data = {"username": TOO_LONG_USERNAME, "password1": VALID_PASSWORD, "password2": VALID_PASSWORD}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_duplicate_username(self):
        """Form is invalid if username is already taken."""
        User.objects.create(username=VALID_USERNAME, password=VALID_PASSWORD)
        form_data = {"username": VALID_USERNAME, "password1": VALID_PASSWORD, "password2": VALID_PASSWORD}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_password_too_long(self):
        """Form is invalid if password exceeds maximum length."""
        form_data = {"username": VALID_USERNAME, "password1": TOO_LONG_PASSWORD, "password2": TOO_LONG_PASSWORD}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_password_too_short(self):
        """Form is invalid if password is shorter than minimum length."""
        form_data = {"username": VALID_USERNAME, "password1": TOO_SHORT_PASSWORD, "password2": TOO_SHORT_PASSWORD}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_password_mismatch(self):
        """Form is invalid if passwords do not match."""
        form_data = {"username": VALID_USERNAME, "password1": "testPass1", "password2": "testPass2"}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_missing_username(self):
        """Form is invalid if username is missing."""
        form_data = {"username": "", "password1": VALID_PASSWORD, "password2": VALID_PASSWORD}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_password1(self):
        """Form is invalid if password1 is missing."""
        form_data = {"username": VALID_USERNAME, "password1": "", "password2": VALID_PASSWORD}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_password2(self):
        """Form is invalid if password2 is missing."""
        form_data = {"username": VALID_USERNAME, "password1": VALID_PASSWORD, "password2": ""}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
