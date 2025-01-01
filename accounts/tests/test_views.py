from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestCustomLoginView(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.tasks_url = reverse('tasks')
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_page_renders_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_redirects_authenticated_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.tasks_url)

    def test_successful_login_redirects_to_tasks(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertRedirects(response, self.tasks_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_failed_login_rerenders_login_page(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class TestRegisterView(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.tasks_url = reverse('tasks')

    def test_registration_page_renders_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_registration_redirects_authenticated_user(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.register_url)
        self.assertRedirects(response, self.tasks_url)

    def test_successful_registration_creates_user_and_redirects_to_tasks(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'strongPassword321',
            'password2': 'strongPassword321',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, self.tasks_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_failed_registration_rerenders_registration_page(self):
        response = self.client.post(self.register_url, {
            'username': '',
            'password1': 'mismatch',
            'password2': 'another',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertFalse(User.objects.filter(username='').exists())
        self.assertContains(response, 'The two password fields didn’t match.')
