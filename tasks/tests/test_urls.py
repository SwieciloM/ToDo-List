from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from tasks.views import TaskListView, TaskCreateView, TaskUpdateView, TaskToggleStatusView, TaskDeleteView


class TestUrlResolution(SimpleTestCase):
    def test_tasks_url_resolves(self):
        url = reverse('tasks')
        self.assertEqual(resolve(url).func.view_class, TaskListView)
    
    def test_task_create_url_resolves(self):
        url = reverse('task-create')
        self.assertEqual(resolve(url).func.view_class, TaskCreateView)

    def test_task_update_url_resolves(self):
        url = reverse('task-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, TaskUpdateView)

    def test_task_toggle_status_url_resolves(self):
        url = reverse('task-toggle-status', args=[1])
        self.assertEqual(resolve(url).func.view_class, TaskToggleStatusView)

    def test_task_delete_url_resolves(self):
        url = reverse('task-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, TaskDeleteView)


class TestUrlReversal(SimpleTestCase):
    def test_reverse_tasks_url(self):
        url = reverse('tasks')
        self.assertEqual(url, '/my-tasks/')

    def test_reverse_task_create_url(self):
        url = reverse('task-create')
        self.assertEqual(url, '/my-tasks/task-create/')

    def test_reverse_task_update_url(self):
        url = reverse('task-update', args=[1])
        self.assertEqual(url, '/my-tasks/task-update/1/')

    def test_reverse_task_toggle_status_url(self):
        url = reverse('task-toggle-status', args=[1])
        self.assertEqual(url, '/my-tasks/task-toggle-status/1/')

    def test_reverse_task_delete_url(self):
        url = reverse('task-delete', args=[1])
        self.assertEqual(url, '/my-tasks/task-delete/1/')
