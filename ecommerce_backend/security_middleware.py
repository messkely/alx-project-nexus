"""
Custom Security Middleware for E-Commerce Backend
"""

import time
import logging
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses
    """
    
    def process_response(self, request, response):
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Add Content Security Policy with support for ReDoc/Swagger documentation
        # Allow blob: for Web Workers used by ReDoc, and worker-src for Web Workers
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' blob:; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "worker-src 'self' blob:; "
            "child-src 'self' blob:; "
            "frame-ancestors 'none';"
        )
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    Simple rate limiting middleware
    """
    
    def process_request(self, request):
        if not hasattr(settings, 'RATE_LIMIT_ENABLED') or not settings.RATE_LIMIT_ENABLED:
            return None
            
        # Get client IP
        ip = self.get_client_ip(request)
        
        # Different limits for different endpoints
        if request.path.startswith('/api/v1/auth/login/'):
            return self.check_rate_limit(ip, 'login', 5, 300)  # 5 attempts per 5 minutes
        elif request.path.startswith('/api/v1/auth/register/'):
            return self.check_rate_limit(ip, 'register', 3, 3600)  # 3 attempts per hour
        elif request.path.startswith('/api/v1/auth/password/reset/'):
            return self.check_rate_limit(ip, 'password_reset', 3, 3600)  # 3 attempts per hour
        elif request.path.startswith('/api/v1/'):
            return self.check_rate_limit(ip, 'api', 100, 60)  # 100 requests per minute
            
        return None
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_rate_limit(self, ip, action, limit, window):
        """Check if the IP has exceeded the rate limit"""
        cache_key = f"rate_limit_{action}_{ip}"
        current_requests = cache.get(cache_key, 0)
        
        if current_requests >= limit:
            logger.warning(f"Rate limit exceeded for IP {ip} on action {action}")
            return HttpResponseForbidden("Rate limit exceeded. Please try again later.")
        
        # Increment the counter
        cache.set(cache_key, current_requests + 1, window)
        return None


class AdminIPWhitelistMiddleware(MiddlewareMixin):
    """
    Restrict admin access to whitelisted IPs
    """
    
    def process_request(self, request):
        if not request.path.startswith('/admin/'):
            return None
            
        # Check if IP whitelist is configured
        allowed_ips = getattr(settings, 'ADMIN_ALLOWED_IPS', [])
        if not allowed_ips:
            return None
            
        client_ip = self.get_client_ip(request)
        
        if client_ip not in allowed_ips:
            logger.warning(f"Unauthorized admin access attempt from IP: {client_ip}")
            return HttpResponseForbidden("Access denied: IP not whitelisted for admin access")
        
        return None
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityLoggingMiddleware(MiddlewareMixin):
    """
    Log security-related events
    """
    
    def process_request(self, request):
        # Log sensitive endpoints access
        sensitive_paths = [
            '/admin/',
            '/api/v1/auth/',
            '/api/v1/orders/',
            '/api/v1/users/',
        ]
        
        for path in sensitive_paths:
            if request.path.startswith(path):
                logger.info(f"Access to sensitive endpoint: {request.path} from IP: {self.get_client_ip(request)}")
                break
        
        return None
    
    def process_response(self, request, response):
        # Log failed authentication attempts
        if response.status_code == 401:
            logger.warning(f"Failed authentication attempt from IP: {self.get_client_ip(request)} for path: {request.path}")
        
        # Log permission denied
        elif response.status_code == 403:
            logger.warning(f"Permission denied for IP: {self.get_client_ip(request)} for path: {request.path}")
        
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class FileUploadSecurityMiddleware(MiddlewareMixin):
    """
    Validate file uploads for security
    """
    
    ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    
    def process_request(self, request):
        if request.method != 'POST' or not request.FILES:
            return None
        
        for field_name, uploaded_file in request.FILES.items():
            # Check file size
            if uploaded_file.size > self.MAX_FILE_SIZE:
                logger.warning(f"File upload too large: {uploaded_file.size} bytes from IP: {self.get_client_ip(request)}")
                return HttpResponseForbidden("File too large")
            
            # Check file extension
            file_extension = self.get_file_extension(uploaded_file.name)
            if file_extension.lower() not in self.ALLOWED_EXTENSIONS:
                logger.warning(f"Blocked file upload with extension: {file_extension} from IP: {self.get_client_ip(request)}")
                return HttpResponseForbidden("File type not allowed")
        
        return None
    
    def get_file_extension(self, filename):
        """Get file extension from filename"""
        return '.' + filename.split('.')[-1] if '.' in filename else ''
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
