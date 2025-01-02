from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from tasks.models import Task
from tasks.forms import TaskCreateForm, TaskUpdateForm


class TestTaskCreateForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_valid_form_data(self):
        """Form should be valid when given all required fields with future due_date."""
        form_data = {
            'title': 'New Task',
            'description': 'This is a test description.',
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_title(self):
        """Form should be invalid if the title is empty (since it's required)."""
        form_data = {
            'title': '',
            'description': 'No title here.',
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        }
        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_past_due_date(self):
        """Form should be invalid if the due_date is in the past (model validation)."""
        form_data = {
            'title': 'Past Task',
            'description': 'This date is in the past.',
            'due_date': (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        }
        form = TaskCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_blank_description_is_valid(self):
        """Description is not required, so a blank description should still be valid."""
        form_data = {
            'title': 'Task with Blank Description',
            'description': '',
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestTaskUpdateForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(
            user=self.user,
            title='Existing Task',
            description='Some description',
            is_completed=False,
            due_date=timezone.now() + timedelta(days=2),
        )

    def test_valid_update_form_data(self):
        """Form should be valid with all required fields (including is_completed)."""
        form_data = {
            'title': 'Updated Task Title',
            'description': 'Updated description',
            'is_completed': True,
            'due_date': (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M'),
        }
        form = TaskUpdateForm(data=form_data, instance=self.task)
        self.assertTrue(form.is_valid())
        updated_task = form.save()
        self.assertEqual(updated_task.title, 'Updated Task Title')
        self.assertTrue(updated_task.is_completed)

    def test_missing_title_in_update_form(self):
        """Title is required; leaving it blank should make the form invalid."""
        form_data = {
            'title': '',
            'description': 'No title here.',
            'is_completed': False,
            'due_date': (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M'),
        }
        form = TaskUpdateForm(data=form_data, instance=self.task)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_past_due_date_in_update_form(self):
        """Form should be invalid if due_date is set in the past."""
        form_data = {
            'title': 'Task with Past Due Date',
            'description': 'Invalid past date.',
            'is_completed': False,
            'due_date': (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        }
        form = TaskUpdateForm(data=form_data, instance=self.task)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_update_is_completed_toggle_only(self):
        """
        Changing only the is_completed field should be valid 
        and the other fields remain unchanged.
        """
        form_data = {
            'title': self.task.title,
            'description': self.task.description,
            'is_completed': True, 
            'due_date': self.task.due_date.strftime('%Y-%m-%dT%H:%M'),
        }
        form = TaskUpdateForm(data=form_data, instance=self.task)
        self.assertTrue(form.is_valid())
        updated_task = form.save()
        self.assertTrue(updated_task.is_completed)
        self.assertEqual(updated_task.title, self.task.title) 
