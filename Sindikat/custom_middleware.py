# middleware.py

from django.contrib.auth.middleware import get_user

class CustomUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = get_user(request)
        return self.get_response(request)
