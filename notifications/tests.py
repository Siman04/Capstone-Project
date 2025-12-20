from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from inventory.models import Item
import datetime
from django.core import management
from django.core.mail import outbox


class NotificationTests(TestCase):

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_expiry_notifications(self):
        u = User.objects.create_user(username='n', email='n@example.com', password='p')
        today = datetime.date.today()
        Item.objects.create(name='soon', user=u, expiry_date=today + datetime.timedelta(days=1))
        from io import StringIO
        out = StringIO()
        management.call_command('send_expiry_notifications', stdout=out)
        output = out.getvalue()
        self.assertIn('Sent to n@example.com', output)
