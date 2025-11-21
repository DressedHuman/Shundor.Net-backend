"""
Tests for the IPBlock app.
These tests ensure the IP blocking middleware and model work as expected.
"""
from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from config.middleware.ip_block_middleware import IPBlockMiddleware
from ip_block.models import IPBlock

class IPBlockMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = IPBlockMiddleware(get_response=lambda r: HttpResponse("OK"))

        # Block a test IP
        IPBlock.objects.create(ip_number="127.0.0.1", reason="Test Block")

    def test_blocked_ip(self):
        request = self.factory.get("/", REMOTE_ADDR="127.0.0.1")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 403)
        self.assertIn("Forbidden", response.content.decode())

    def test_allowed_ip(self):
        request = self.factory.get("/", REMOTE_ADDR="192.168.1.1")
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "OK")
