from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from inventory.models import Item
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Send expiry notifications to users for items expiring soon (3d, 1d, 0d)'

    def handle(self, *args, **options):
        today = timezone.localdate()
        alert_days = [3, 1, 0]
        targets = [today + timedelta(days=d) for d in alert_days]

        items = Item.objects.filter(expiry_date__in=targets).select_related('user')

        by_user = {}
        for it in items:
            days_left = (it.expiry_date - today).days
            by_user.setdefault(it.user.email, []).append((it, days_left))

        from django.core.mail import EmailMessage, get_connection

        connection = get_connection()
        for email, items_list in by_user.items():
            if not email:
                continue
            subject = 'Expiry reminders for your items'
            lines = []
            for it, days_left in items_list:
                lines.append(f"- {it.name}: expires in {days_left} day(s) on {it.expiry_date}")
            message = "Hello,\n\nThe following items are expiring soon:\n\n" + "\n".join(lines) + "\n\nRegards\nSmart Expiry Tracker"
            msg = EmailMessage(subject=subject, body=message, from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com'), to=[email])
            connection.send_messages([msg])
            self.stdout.write(self.style.SUCCESS(f"Sent to {email}: {len(items_list)} items"))
