import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pythonservice.settings')
django.setup()

from rest_framework import status
from django.test import TestCase
from customers.models import Customers
from orders.models import Orders
from rest_framework.test import APIClient


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customers.objects.create(name='Customer Test ', code='C001', phone_number='+254707458414')
        self.order = Orders.objects.create(customer=self.customer, item='Test Item', amount=1)

        # Include OAuth2 authentication headers
        self.client.credentials(HTTP_AUTHORIZATION='Bearer BLwUfa013yOIhCHUQpjShL4J8vW9uP')

    def tearDown(self):
        Customers.objects.all().delete()

    def test_customer_create_view(self):
        response = self.client.post('/api/customer/',
                                    {'name': 'New Customer', 'code': 'CC001', 'phone_number': '+254707458414'})
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customers.objects.count(), 3)
        self.assertEqual(Customers.objects.get(code='CC001').name, 'New Customer')

    def test_order_create_view(self):
        response = self.client.post('/api/order/', {'customer': self.customer.id, 'item': 'New Item', 'amount': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Orders.objects.count(), 3)
        self.assertEqual(Orders.objects.get(item='New Item').amount, 2)
