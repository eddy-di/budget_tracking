from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from wallet.sitemaps import ExpenseSitemap, IncomeSitemap
from django.conf import settings
from django.conf.urls.static import static
from account.views import home_page


sitemaps = {
    'expenses': ExpenseSitemap,
    'incomes': IncomeSitemap,
}

urlpatterns = [
    path('', home_page, name='home'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('wallet-api/', include('wallet.api.urls', namespace='wallet_api')),
    path('account-api/', include('account.api.urls', namespace='account_api')),
    path('auth-api/', include('rest_framework.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('wallet/', include('wallet.urls', namespace='wallet')),
    path('sitemaps.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # swagger schemas,
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                          document_root=settings.MEDIA_ROOT)