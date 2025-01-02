from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task


class TestTaskListView(TestCase):
    def setUp(self):
        self.list_url = reverse('tasks')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task1 = Task.objects.create(
            user=self.user,
            title='Task 1',
            description='',
            is_completed=False,
            due_date=timezone.now() + timedelta(hours=10)
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            user=self.user,
            is_completed=True,
            due_date=timezone.now() + timedelta(hours=5)
        )
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.task_other_user = Task.objects.create(
            user=other_user,
            title='Task 3'
        )

    def test_list_view_redirects_if_not_logged_in(self):
        """
        The TaskListView is login-required, so an anonymous user should
        be redirected to the login page.
        """
        response = self.client.get(self.list_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{reverse('login')}?next={self.list_url}")

    def test_list_view_shows_only_user_tasks(self):
        """Logged in user should see only their tasks, not tasks of other users."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html') 
        tasks = response.context['tasks']

        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)
        self.assertNotIn(self.task_other_user, tasks)

    def test_list_view_context_counts_and_hours_left(self):
        """
        Check presence of the additional context data:
        - `incompleted_count`
        - `completed_count`
        - `hours_left`
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['incompleted_count'], 1)
        self.assertEqual(response.context['completed_count'], 1) 

        tasks = response.context['tasks']
        for task in tasks:
            if task.due_date:
                self.assertIsNotNone(task.hours_left)
            else:
                self.assertIsNone(task.hours_left)

    def test_list_view_search_functionality(self):
        """If a 'search-area' query param is provided, the tasks should be filtered."""
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(self.list_url, {'search-area': 'Task 1'})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertIn(self.task1, tasks)
        self.assertNotIn(self.task2, tasks)

        response = self.client.get(self.list_url, {'clear': 'true'})
        tasks = response.context['tasks']
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)


class TestTaskCreateView(TestCase):
    def setUp(self):
        self.create_url = reverse('task-create')
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_view_redirects_if_not_logged_in(self):
        """
        The TaskCreateView is login-required, so an anonymous user should
        be redirected to the login page.
        """
        response = self.client.get(self.create_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{reverse('login')}?next={self.create_url}")

    def test_create_view_GET_logged_in_user(self):
        """Logged in user should see the form to create a task."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html') 
        self.assertEqual(response.context['form_type'], 'create')

    def test_create_view_POST_valid_data(self):
        """
        Posting valid data should create a new task for the user,
        and redirect to the tasks list.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.create_url, {
            'title': 'New Task'
        })
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(title='New Task', user=self.user).exists())

    def test_create_view_POST_invalid_data(self):
        """
        If the form is invalid, the view should re-render the page
        with errors and not create a task.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.create_url, {
            'title': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertFalse(Task.objects.filter(title='').exists())


class TestTaskUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(title='Initial Title', user=self.user)
        self.update_url = reverse('task-update', kwargs={'pk': self.task.pk})

    def test_update_view_redirects_if_not_logged_in(self):
        """
        The TaskUpdateView is login-required, so an anonymous user should
        be redirected to the login page.
        """
        response = self.client.get(self.update_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{reverse('login')}?next={self.update_url}")

    def test_update_view_GET_logged_in_user(self):
        """Logged in user should see the form to update their task."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertEqual(response.context['form_type'], 'update')
        self.assertEqual(response.context['form'].instance, self.task)

    def test_update_view_POST_valid_data(self):
        """Posting valid data should update the task and redirect to the task list."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.update_url, {
            'title': 'Updated Title'
        })
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')

    def test_update_view_with_different_user(self):
        """
        A user who doesn't own the task should generally get a 404 or be prevented
        from updating it.
        """
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 404)


class TestTaskToggleStatusView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(title='Toggle Test', user=self.user, is_completed=False)
        self.toggle_url = reverse('task-toggle-status', kwargs={'pk': self.task.pk})

    def test_toggle_view_redirects_if_not_logged_in(self):
        """
        The TaskToggleStatusView is login-required, so an anonymous user should
        be redirected to the login page.
        """
        response = self.client.post(self.toggle_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{reverse('login')}?next={self.toggle_url}")

    def test_toggle_view_POST_toggles_task(self):
        """
        Posting to the toggle endpoint should flip the is_completed field
        and redirect to 'tasks'.
        """
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.toggle_url)
        self.assertRedirects(response, reverse('tasks'))

        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

        response = self.client.post(self.toggle_url)
        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)

    def test_toggle_view_POST_invalid_user(self):
        """
        A user who doesn't own the task should generally get a 404 or be prevented
        from toggling it.
        """
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.post(self.toggle_url)
        self.assertEqual(response.status_code, 404)


class TestTaskDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(title='Delete Me', user=self.user)
        self.delete_url = reverse('task-delete', kwargs={'pk': self.task.pk})

    def test_delete_view_redirects_if_not_logged_in(self):
        """
        The TaskDeleteView is login-required, so an anonymous user should
        be redirected to the login page.
        """
        response = self.client.get(self.delete_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{reverse('login')}?next={self.delete_url}")

    def test_delete_view_GET_confirm_page(self):
        """By default, Django's DeleteView uses a GET to display the "confirm delete" page."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')

    def test_delete_view_POST_deletes_task(self):
        """Once confirmed, the POST request should delete the task and redirect."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_delete_view_invalid_user(self):
        """A user who doesn't own the task should not be able to delete it."""
        other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 404)
