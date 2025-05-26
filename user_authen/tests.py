from django.test import TestCase
from .models import CustomUser

class CustomUserModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            name='Test User',
            phone_number='1234567890',
            password='testpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertEqual(self.user.role, 'agent')

    def test_superuser_creation(self):
        superuser = CustomUser.objects.create_superuser(
            email='admin@example.com',
            name='Admin User',
            phone_number='0987654321',
            password='adminpassword',
            role='admin'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'Test User (agent)')