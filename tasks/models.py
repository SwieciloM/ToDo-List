from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


def validate_due_date(date):
    """Validator to ensure the due_date is not set in the past."""
    if date and date < timezone.now():
        raise ValidationError('Due date cannot be in the past.')


class Task(models.Model):
    """Model representing a task associated with a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True, validators=[validate_due_date])

    class Meta:
        """Meta options for the Task model."""
        ordering = ['-creation_date']  # Default ordering: Newest tasks first
        verbose_name = "Task"  # Name displayed in the admin interface
        verbose_name_plural = "Tasks"

    def __str__(self):
        """String representation of the task model."""
        return self.title
     

