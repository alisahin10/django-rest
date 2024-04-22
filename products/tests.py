from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product


class AuthenticationPermissionsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alisahin', password='admin123*')
        self.staff_user = User.objects.create_user(username='staff', password='admin123*', is_staff=True)
        self.admin_user = User.objects.create_user(username='admin', password='admin123*', is_superuser=True)
        self.product_data = {'title': 'Test Product', 'content': 'Test Content', 'price': 10.00, 'public': True}
        self.product_data_put = {'title': 'Test Product', 'content': 'Test Content'}
        self.product = Product.objects.create(user=self.user, **self.product_data)
        self.url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})
        self.edit_url = reverse('product-edit', kwargs={'pk': self.product.pk})

    def test_authenticated_access(self):
        self.client.login(username='admin', password='admin123*')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_access(self):
        self.client.login(username='admin', password='admin123*')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_access(self):
        self.client.login(username='admin', password='admin123*')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_only_permission(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_write_permission(self):
        self.client.login(username='admin', password='admin123*')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_only_permission(self):
        self.client.login(username='admin', password='admin123*')
        response = self.client.post(self.url, self.product_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST),


class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='alisahin', password='admin123*')
        self.staff_user = User.objects.create_user(username='staff', password='admin123*', is_staff=True)
        self.admin_user = User.objects.create_user(username='admin', password='admin123*', is_superuser=True)
        self.product_data = {'title': 'Test Product', 'content': 'Test Content', 'price': 10.00, 'public': True}
        # Create a product
        self.client.login(username='admin', password='admin123*')
        response = self.client.post(reverse('product-list'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Ensure product creation was successful
        # Fetch the created product
        self.product = Product.objects.first()

    def test_create_product(self):
        self.client.login(username='admin', password='admin123*')
        response = self.client.post(reverse('product-list'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        self.client.login(username='admin', password='admin123*')
        updated_data = {'title': 'Updated Test Product', 'content': 'Updated Test Content', 'price': 15.00, 'public': False}
        response = self.client.put(reverse('product-edit', kwargs={'pk': self.product.pk}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        updated_product = Product.objects.get(pk=self.product.pk)

class ValidationTesting(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alisahin', password='admin123*')
        self.staff_user = User.objects.create_user(username='staff', password='admin123*', is_staff=True)
        self.admin_user = User.objects.create_user(username='admin', password='admin123*', is_superuser=True)
        self.product_data_valid = {'title': 'Test Product', 'content': 'Test Content', 'price': 10.00, 'public': True}
        self.product_data_invalid = {'title': '', 'content': 'Test Content', 'price': 10.00, 'public': True}
        self.url = reverse('product-list')

    def test_valid_data(self):
        self.client.login(username='admin', password='admin123*')
        response = self.client.post(self.url, self.product_data_valid, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        self.client.login(username='alisahin', password='admin123*')
        response = self.client.post(self.url, self.product_data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
