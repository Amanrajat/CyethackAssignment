from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from threats.views import EventViewSet, AlertViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# DRF Router
router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'alerts', AlertViewSet)

# Swagger Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Cyethack Threat Monitoring API",
        default_version='v1',
        description="Backend APIs for Threat Monitoring & Alert Management",
        terms_of_service="https://www.cyethack.com/terms/",
        contact=openapi.Contact(email="security@cyethack.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # APIs
    path('api/', include(router.urls)),

    # Swagger / Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
