from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestCustomLoginView(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.tasks_url = reverse('tasks')
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_page_renders_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_authenticated_user_redirects_to_tasks(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.tasks_url)

    def test_successful_login_redirects_to_tasks(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'password123'})
        self.assertRedirects(response, self.tasks_url)

    def test_failed_login_renders_errors(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'Please enter a correct username and password.')


class TestRegisterView(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.tasks_url = reverse('tasks')

    def test_registration_page_renders_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_authenticated_user_redirects_to_tasks(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.register_url)
        self.assertRedirects(response, self.tasks_url)

    def test_successful_registration_creates_user_and_redirects_to_tasks(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })
        self.assertRedirects(response, self.tasks_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_failed_registration_renders_errors(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, 'The two password fields didn’t match.')
