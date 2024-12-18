from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('my-tasks/')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('tasks')


class CustomRegisterView():
    pass