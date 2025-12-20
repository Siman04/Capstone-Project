from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from inventory.models import Item
import datetime


class DashboardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='u', password='p')
        self.client.force_authenticate(user=self.user)

    def test_dashboard_summary_counts(self):
        today = datetime.date.today()
        Item.objects.create(name='expired', user=self.user, expiry_date=today - datetime.timedelta(days=1))
        Item.objects.create(name='soon', user=self.user, expiry_date=today + datetime.timedelta(days=3))
        Item.objects.create(name='safe', user=self.user, expiry_date=today + datetime.timedelta(days=30))

        resp = self.client.get('/api/dashboard/summary/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['expired_count'], 1)
        self.assertEqual(data['expiring_soon_count'], 1)
        self.assertEqual(data['safe_count'], 1)

    def test_dashboard_filters(self):
        today = datetime.date.today()
        cat = None
        # create a category for filtering
        from inventory.models import Category
        cat = Category.objects.create(name='Food', user=self.user)
        Item.objects.create(name='milk', user=self.user, expiry_date=today + datetime.timedelta(days=2), category=cat)
        Item.objects.create(name='bread', user=self.user, expiry_date=today + datetime.timedelta(days=30), category=cat)

        # filter by status=soon
        resp = self.client.get('/api/dashboard/summary/?status=soon')
        data = resp.json()
        self.assertIn('expiring_soon_count', data)

        # filter by name substring
        resp2 = self.client.get('/api/dashboard/summary/?name=milk')
        data2 = resp2.json()
        self.assertEqual(data2['expiring_soon_count'], 1)

        # filter by category
        resp3 = self.client.get(f'/api/dashboard/summary/?category_id={cat.id}')
        data3 = resp3.json()
        self.assertEqual(data3['expiring_soon_count'] + data3['safe_count'] + data3['expired_count'], 2)
