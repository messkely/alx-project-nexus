from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from .health_views import health_check as aws_health_check, readiness_check, liveness_check

schema_view = get_schema_view(
   openapi.Info(
      title="E-Commerce API",
      default_version='v1',
      description="API documentation for the e-commerce backend",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def health_check(request):
    """Simple health check endpoint for Docker"""
    return JsonResponse({'status': 'healthy', 'service': 'ecommerce-api'})

urlpatterns = [
   path('admin/', admin.site.urls),
   
   # Health check endpoints for AWS/Docker
   path('health/', aws_health_check, name='aws-health-check'),
   path('health/readiness/', readiness_check, name='readiness-check'),
   path('health/liveness/', liveness_check, name='liveness-check'),
   path('api/v1/health/', health_check, name='health-check'),  # Legacy health check
    
   # Authentication & User Management URLs
   path('api/v1/auth/', include('users.urls')),
   path('api/v1/users/', include('users.urls')),  # For user profile management
    
   # Core E-commerce APIs
   path('api/v1/', include('catalog.urls')),  # This includes both products/ and categories/ paths
   path('api/v1/cart/', include('cart.urls')),
   path('api/v1/orders/', include('orders.urls')),
   path('api/v1/reviews/', include('reviews.urls')),

   # API Documentation URLs
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
   path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('api/v1/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
