from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = 'accounts/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('my-tasks/')
        return super().get(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class CustomLogoutView():
    pass

class CustomRegisterView():
    pass