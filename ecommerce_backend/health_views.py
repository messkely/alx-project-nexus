"""
AWS Health Check Views for ALX E-Commerce Backend
"""

import os
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.core.cache import cache
import django

@csrf_exempt
@require_http_methods(["GET", "HEAD"])
def health_check(request):
    """
    Health check endpoint for AWS ALB/API Gateway
    """
    try:
        # Check database connection
        db_conn = connections['default']
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "healthy"
        
        # Check cache connection
        try:
            cache.set('health_check', 'ok', 10)
            cache_result = cache.get('health_check')
            cache_status = "healthy" if cache_result == 'ok' else "unhealthy"
        except Exception:
            cache_status = "unhealthy"
        
        return JsonResponse({
            'status': 'healthy',
            'service': 'alx-ecommerce-backend',
            'version': '1.0.0',
            'django_version': django.get_version(),
            'database': db_status,
            'cache': cache_status,
            'environment': 'aws-lambda' if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ else 'local'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'service': 'alx-ecommerce-backend',
            'error': str(e)
        }, status=500)


@csrf_exempt  
@require_http_methods(["GET"])
def readiness_check(request):
    """
    Readiness check for Kubernetes/container orchestration
    """
    try:
        from django.contrib.auth.models import User
        # Simple query to check if database is ready
        User.objects.count()
        
        return JsonResponse({
            'status': 'ready',
            'service': 'alx-ecommerce-backend'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'not_ready',
            'service': 'alx-ecommerce-backend',
            'error': str(e)
        }, status=503)


@csrf_exempt
@require_http_methods(["GET"])
def liveness_check(request):
    """
    Liveness check for container orchestration
    """
    return JsonResponse({
        'status': 'alive',
        'service': 'alx-ecommerce-backend'
    })
