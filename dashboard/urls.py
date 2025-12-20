from django.urls import path
from .views import DashboardSummaryView, DemoView

urlpatterns = [
	path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
	path('demo/', DemoView.as_view(), name='dashboard-demo'),
]
