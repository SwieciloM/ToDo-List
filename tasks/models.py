from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # null and blank are temporary True
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        # Orders tasks by completion status (False first, then True)
        ordering = ['is_completed']

    def clean(self):
        # Ensure due_date is not before creation_date
        if self.due_date and self.due_date < self.creation_date:
            raise ValidationError("Due date cannot be earlier than creation date.")
        super().clean()

    def __str__(self):
        # Return task title as string representation
        return self.title
     

