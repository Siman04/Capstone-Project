from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Medicine', 'Medicine'),
        ('Skincare', 'Skincare'),
        ('Cleaning', 'Cleaning'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    purchase_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField()
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='items/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
