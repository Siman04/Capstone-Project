from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from inventory.models import Category, Item
from django.urls import reverse
from rest_framework import status
import datetime


class InventoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user1', password='pass12345')
        self.user2 = User.objects.create_user(username='user2', password='pass12345')
        self.client.force_authenticate(user=self.user)

    def test_create_category_and_item(self):
        # create category
        resp = self.client.post('/api/inventory/categories/', {'name': 'Food'})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        category_id = resp.data['id']

        # create item using category_id
        expiry = (datetime.date.today() + datetime.timedelta(days=10)).isoformat()
        item_data = {
            'name': 'Milk',
            'category_id': category_id,
            'quantity': 1,
            'purchase_date': datetime.date.today().isoformat(),
            'expiry_date': expiry,
            'notes': 'Test milk'
        }
        resp2 = self.client.post('/api/inventory/items/', item_data, format='json')
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp2.data['name'], 'Milk')

    def test_users_cannot_use_other_users_category(self):
        cat = Category.objects.create(name='Med', user=self.user2)
        expiry = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
        item_payload = {
            'name': 'Pill',
            'category_id': cat.id,
            'expiry_date': expiry
        }
        resp = self.client.post('/api/inventory/items/', item_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_item_list_scoped_to_user(self):
        Item.objects.create(name='A', user=self.user, expiry_date=datetime.date.today())
        Item.objects.create(name='B', user=self.user2, expiry_date=datetime.date.today())
        resp = self.client.get('/api/inventory/items/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        names = [it['name'] for it in resp.data]
        self.assertIn('A', names)
        self.assertNotIn('B', names)

    def test_export_csv(self):
        Item.objects.create(name='C', user=self.user, expiry_date=datetime.date.today())
        resp = self.client.get('/api/inventory/items/export/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'text/csv')
        content = resp.content.decode('utf-8')
        self.assertIn('C', content)
