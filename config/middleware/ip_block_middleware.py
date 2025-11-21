# middleware/ip_block_middleware.py
from django.http import JsonResponse
from ip_block.models import IPBlock

class IPBlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # check if IP is blocked
        if IPBlock.objects.filter(ip_number=ip).exists():
            return JsonResponse({"detail": "Your IP is blocked."}, status=403)

        return self.get_response(request)

    def get_client_ip(self, request):
        """Support proxy setups"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
