from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer


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
