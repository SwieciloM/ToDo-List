from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .forms import TaskCreateForm
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['incompleted_count'] = context['tasks'].filter(is_completed=False).count()
        context['completed_count'] = context['tasks'].filter(is_completed=True).count()

        # Check which button was pressed
        if 'clear' in self.request.GET:
            # Clear button pressed, no search filter
            search_input = ''
        else:
            # Use the search-area parameter if provided
            search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        current_time = timezone.now()
        for task in context['tasks']:
            if task.due_date:
                task.hours_left = (task.due_date - current_time).total_seconds() / 3600
            else:
                task.hours_left = None
        
        context['search_input'] = search_input

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'is_completed', 'due_date']
    success_url = reverse_lazy('tasks')
    

class TaskToggleStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.is_completed = not task.is_completed
        task.save()
        return redirect('tasks')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
