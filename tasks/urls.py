from django.urls import path
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskToggleStatusView

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('task-toggle-status/<int:pk>/', TaskToggleStatusView.as_view(), name='task-toggle-status'),
]