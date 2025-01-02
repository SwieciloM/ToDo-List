from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import timedelta
from tasks.models import Task
import time


class TestTaskModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_valid_task(self):
        """Check that creating a valid task succeeds without errors."""
        task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task.',
            due_date=timezone.now() + timedelta(days=1)
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertFalse(task.is_completed)
        self.assertEqual(task.user, self.user)
        self.assertIsNotNone(task.creation_date)

    def test_due_date_cannot_be_in_the_past(self):
        """
        Attempting to set a past due date should raise ValidationError
        when the model is cleaned or saved with full validation.
        """
        past_date = timezone.now() - timedelta(days=1)
        task = Task(
            user=self.user,
            title='Invalid Task',
            due_date=past_date
        )
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_str_representation(self):
        """The __str__ method should return the title of the task."""
        task = Task.objects.create(
            user=self.user,
            title='My Important Task'
        )
        self.assertEqual(str(task), 'My Important Task')

    def test_default_ordering(self):
        """
        The Meta ordering is ['-creation_date'], so the newest Task should come first.
        We create tasks in succession and check their order.
        """
        task1 = Task.objects.create(
            user=self.user,
            title='First Created' 
        )
        time.sleep(0.1) 
        task2 = Task.objects.create(
            user=self.user,
            title='Second Created'
        )

        tasks = list(Task.objects.all())
        self.assertEqual(tasks[0], task2)
        self.assertEqual(tasks[1], task1)
