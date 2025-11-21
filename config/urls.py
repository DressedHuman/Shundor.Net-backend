from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    # Djoser Auth Urls
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),
    path("banner/", include("banner.urls")),
    path("", include("user.urls")),
    path("", include("product.urls")),
    path("", include("cart.urls")),
    path("", include("brand.urls")),
    path("", include("contact.urls")),
    path("", include("category.urls")),
    path("", include("order.urls")),
    path("", include("review.urls")),
    path("", include("shipping_charge.urls")),
    path("", include("wishlist.urls")),
    path("", include("site_setting.urls")),
    path('', include('fraud_api.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
