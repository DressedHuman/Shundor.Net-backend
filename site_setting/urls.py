
# API endpoints for site settings
from django.urls import path
from .views import SiteSettingListCreateAPIView, SiteSettingDetailAPIView

urlpatterns = [
	path('site-settings/', SiteSettingListCreateAPIView.as_view(), name='sitesetting-list-create'),
	path('site-settings/<int:pk>/', SiteSettingDetailAPIView.as_view(), name='sitesetting-detail'),
]
