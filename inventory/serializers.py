from rest_framework import serializers
from .models import Item, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):
    # Accept category id for writes and provide nested data for reads
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Item
        fields = ('id', 'name', 'category', 'category_id', 'quantity', 'purchase_date', 'expiry_date', 'notes', 'image')
        read_only_fields = ('id', 'category')

    def validate(self, attrs):
        # ensure category belongs to the user if provided
        category = attrs.get('category')
        request = self.context.get('request')
        if category and request and category.user != request.user:
            raise serializers.ValidationError({'category_id': 'Category does not belong to the authenticated user.'})
        return attrs
