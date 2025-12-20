from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer
from rest_framework.decorators import action
from django.http import HttpResponse
import csv


class IsOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user).order_by('expiry_date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export user's items as CSV"""
        qs = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="items.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'name', 'category', 'quantity', 'purchase_date', 'expiry_date', 'notes'])
        for it in qs:
            writer.writerow([it.id, it.name, it.category.name if it.category else '', it.quantity, it.purchase_date, it.expiry_date, it.notes])
        return response
