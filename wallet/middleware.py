from django.http import HttpResponseForbidden
from django.urls import resolve
from django.shortcuts import redirect
from django.conf import settings

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before the view is called
        if not request.user.is_authenticated:
            wallet = settings.WALLET_REQUIRE_LOGIN_MIDDLEWARE
            if request.path_info.startswith(wallet):
                return redirect('account:redirect')

        return self.get_response(request)
