from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    """Handles user login with redirection for authenticated users."""
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirect to the 'tasks' page upon successful login."""
        return reverse_lazy('tasks')


class RegisterView(FormView):
    """Handles user registration and automatic login."""
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        """Save the user and log them in if the form is valid."""
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        """Redirect authenticated users to 'tasks' or show the form."""
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(self.request, *args, **kwargs)
