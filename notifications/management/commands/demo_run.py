from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from inventory.models import Category, Item
from datetime import date, timedelta
import csv
from io import StringIO
from django.core import management


class Command(BaseCommand):
    help = 'Run a demo sequence: create a user, tokens, category, item, show dashboard, export CSV, and run notifications.'

    def handle(self, *args, **options):
        # create demo user
        user, created = User.objects.get_or_create(username='demo_user', defaults={'email': 'demo@example.com'})
        if created:
            user.set_password('demopass123')
            user.save()
        self.stdout.write(self.style.SUCCESS(f"User: {user.username} (created={created})"))

        # generate tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        self.stdout.write('Access token: ' + access)

        # create category
        cat, ccreated = Category.objects.get_or_create(name='Demo Category', user=user)
        self.stdout.write(self.style.SUCCESS(f"Category: {cat.name} (created={ccreated}) id={cat.id}"))

        # create item
        expiry = date.today() + timedelta(days=3)
        item = Item.objects.create(user=user, name='Demo Milk', category=cat, quantity=1, purchase_date=date.today(), expiry_date=expiry, notes='Demo')
        self.stdout.write(self.style.SUCCESS(f"Created item: {item.name} expiry={item.expiry_date} id={item.id}"))

        # dashboard summary
        today = date.today()
        soon_threshold = today + timedelta(days=7)
        items = Item.objects.filter(user=user)
        expired = items.filter(expiry_date__lt=today)
        soon = items.filter(expiry_date__gte=today, expiry_date__lte=soon_threshold)
        safe = items.filter(expiry_date__gt=soon_threshold)
        self.stdout.write('Dashboard summary:')
        self.stdout.write(f'  expired_count={expired.count()}')
        self.stdout.write(f'  expiring_soon_count={soon.count()}')
        self.stdout.write(f'  safe_count={safe.count()}')

        # CSV export to string
        buf = StringIO()
        writer = csv.writer(buf)
        writer.writerow(['id', 'name', 'category', 'quantity', 'purchase_date', 'expiry_date', 'notes'])
        for it in items:
            writer.writerow([it.id, it.name, it.category.name if it.category else '', it.quantity, it.purchase_date, it.expiry_date, it.notes])
        csv_content = buf.getvalue()
        self.stdout.write('CSV export:\n' + csv_content)

        # run notifications command
        self.stdout.write('Running send_expiry_notifications:')
        management.call_command('send_expiry_notifications', stdout=self.stdout)
