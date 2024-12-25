from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone


def validate_due_date(date):
    # Ensure due_date is not before creation_date
    if date and date < timezone.now():
        raise ValidationError('Due date cannot be in the past.')


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True, validators=[validate_due_date])

    class Meta:
        # Orders tasks by completion status (False first, then True)
        ordering = ['-creation_date']

    def __str__(self):
        # Return task title as string representation
        return self.title
     

