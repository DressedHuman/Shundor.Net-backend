from django.urls import path
from .views import (
    ContactListView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView
)

urlpatterns = [
    path('contacts/', ContactListView.as_view(), name='contact-list'),
    path('contacts/create/', ContactCreateView.as_view(), name='contact-create'),
    path('contacts/<int:id>/update/', ContactUpdateView.as_view(), name='contact-update'),
    path('contacts/<int:id>/delete/', ContactDeleteView.as_view(), name='contact-delete'),
]
