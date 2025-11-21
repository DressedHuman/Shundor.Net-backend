from django.urls import path
from .views import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brands/create/', BrandCreateView.as_view(), name='brand-create'),
    path('brands/<str:id>/update/', BrandUpdateView.as_view(), name='brand-update'),
    path('brands/<str:id>/delete/', BrandDeleteView.as_view(), name='brand-delete'),
]
