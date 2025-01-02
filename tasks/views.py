from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .forms import TaskCreateForm, TaskUpdateForm
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    """Displays the list of tasks for the logged-in user."""
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        """Adds filtered tasks, counts, and search functionality to the context."""
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['incompleted_count'] = context['tasks'].filter(is_completed=False).count()
        context['completed_count'] = context['tasks'].filter(is_completed=True).count()

        # Handle search and clear filter functionality
        search_input = self.request.GET.get('search-area', '') if 'clear' not in self.request.GET else ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input

        # Calculate hours left for each task
        current_time = timezone.now()
        for task in context['tasks']:
            if task.due_date:
                task.hours_left = (task.due_date - current_time).total_seconds() / 3600
            else:
                task.hours_left = None
        
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """Handles task creation."""
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        """Associates the created task with the logged-in user."""
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Adds a form type identifier for the template."""
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'create'
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    """Handles task updates."""
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        """Only return tasks owned by the current user."""
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Adds a form type identifier for the template."""
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'update'
        return context
    

class TaskToggleStatusView(LoginRequiredMixin, View):
    """Toggles the completion status of a task."""
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.is_completed = not task.is_completed
        task.save()
        return redirect('tasks')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """Handles task deletion."""
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        """Only return tasks owned by the current user."""
        return Task.objects.filter(user=self.request.user)
