from django import forms
from .models import Task


class TaskCreateForm(forms.ModelForm):
    """Form for creating a new task with title, description, and due date."""

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "e.g. Read a book"
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': "e.g. Finish reading 'Atomic Habits' by the end of the week"
            }),
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }), 
        }


class TaskUpdateForm(forms.ModelForm):
    """Form for updating an existing task (including status)"""

    class Meta:
        model = Task
        fields = ['title', 'description', 'is_completed', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': "This field cannot be empty"
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': "No description provided"
            }), 
            'due_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }), 
        }
