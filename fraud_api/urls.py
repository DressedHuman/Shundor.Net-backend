
# API endpoints for fraud APIs
from django.urls import path
from .views import FraudAPIListCreateView, FraudAPIDetailView

urlpatterns = [
	path('fraud-apis/', FraudAPIListCreateView.as_view(), name='fraudapi-list-create'),
	path('fraud-apis/<int:pk>/', FraudAPIDetailView.as_view(), name='fraudapi-detail'),
]






