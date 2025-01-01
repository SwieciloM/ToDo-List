from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView


class TestUrlResolution(SimpleTestCase):
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)


class TestUrlReversal(SimpleTestCase):
    def test_reverse_login_url(self):
        url = reverse('login')
        self.assertEqual(url, '/')

    def test_reverse_logout_url(self):
        url = reverse('logout')
        self.assertEqual(url, '/logout/')

    def test_reverse_register_url(self):
        url = reverse('register')
        self.assertEqual(url, '/register/')
