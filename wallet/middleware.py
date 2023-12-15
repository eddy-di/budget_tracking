from django.http import HttpResponseForbidden
from django.urls import resolve
from django.shortcuts import redirect
from django.conf import settings

class RequireLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before the view is called
        
        if request.user.is_authenticated:
            has_wallet = request.user.wallet_users.exists() # Check if the user has a wallet            
            current_view = resolve(request.path_info).url_name # Get the current view            
            exempt_views = ['add_wallet'] # Define views that do not require a wallet check
            if not has_wallet and current_view not in exempt_views:
                return redirect('wallet:add_wallet')

        if not request.user.is_authenticated:
            wallet = settings.WALLET_REQUIRE_LOGIN_MIDDLEWARE
            if request.path_info.startswith(wallet):
                return redirect('account:redirect')

        return self.get_response(request)
