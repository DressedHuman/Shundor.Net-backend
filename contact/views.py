

"""
Views for handling contact-related API requests.
"""
from rest_framework import generics, permissions
from .models import Contact
from .serializers import ContactSerializer

# List all contacts - any authenticated user
class ContactListView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

# Create a new contact - admin only
class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]

# Update a contact by ID - admin only
class ContactUpdateView(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

# Delete a contact by ID - admin only
class ContactDeleteView(generics.DestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
