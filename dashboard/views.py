from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from inventory.models import Item
from inventory.serializers import ItemSerializer
from django.utils import timezone
from datetime import timedelta


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        soon_threshold = today + timedelta(days=7)

        items = Item.objects.filter(user=request.user)

        # optional filters
        status = request.query_params.get('status')  # expired | soon | safe
        category_id = request.query_params.get('category_id')
        name = request.query_params.get('name')

        if category_id:
            items = items.filter(category_id=category_id)
        if name:
            items = items.filter(name__icontains=name)

        expired_qs = items.filter(expiry_date__lt=today).order_by('expiry_date')
        expiring_soon_qs = items.filter(expiry_date__gte=today, expiry_date__lte=soon_threshold).order_by('expiry_date')
        safe_qs = items.filter(expiry_date__gt=soon_threshold).order_by('expiry_date')

        data = {
            'expired_count': expired_qs.count(),
            'expiring_soon_count': expiring_soon_qs.count(),
            'safe_count': safe_qs.count(),
            'expired': ItemSerializer(expired_qs, many=True).data,
            'expiring_soon': ItemSerializer(expiring_soon_qs, many=True).data,
            'safe': ItemSerializer(safe_qs, many=True).data,
        }

        # If a specific status filter is provided, return only that bucket
        if status == 'expired':
            return Response({'expired_count': data['expired_count'], 'expired': data['expired']})
        if status == 'soon':
            return Response({'expiring_soon_count': data['expiring_soon_count'], 'expiring_soon': data['expiring_soon']})
        if status == 'safe':
            return Response({'safe_count': data['safe_count'], 'safe': data['safe']})

        return Response(data)


class DemoView(APIView):
    """Public demo endpoint returning sample dashboard data (no auth required)."""
    permission_classes = [AllowAny]

    def get(self, request):
        today = timezone.localdate()
        sample_items = [
            {
                "id": 1,
                "name": "Milk",
                "category": {"id": 1, "name": "Dairy"},
                "quantity": 2,
                "purchase_date": str(today - timedelta(days=2)),
                "expiry_date": str(today + timedelta(days=3)),
                "notes": "2L"
            },
            {
                "id": 2,
                "name": "Eggs",
                "category": {"id": 2, "name": "Poultry"},
                "quantity": 12,
                "purchase_date": str(today - timedelta(days=5)),
                "expiry_date": str(today - timedelta(days=1)),
                "notes": "Free-range"
            },
            {
                "id": 3,
                "name": "Canned Beans",
                "category": {"id": 3, "name": "Canned"},
                "quantity": 6,
                "purchase_date": str(today - timedelta(days=30)),
                "expiry_date": str(today + timedelta(days=365)),
                "notes": ""
            }
        ]

        expired = [i for i in sample_items if i['expiry_date'] < str(today)]
        expiring_soon = [i for i in sample_items if str(today) <= i['expiry_date'] <= str(today + timedelta(days=7))]
        safe = [i for i in sample_items if i['expiry_date'] > str(today + timedelta(days=7))]

        data = {
            'expired_count': len(expired),
            'expiring_soon_count': len(expiring_soon),
            'safe_count': len(safe),
            'expired': expired,
            'expiring_soon': expiring_soon,
            'safe': safe,
        }

        return Response(data)
