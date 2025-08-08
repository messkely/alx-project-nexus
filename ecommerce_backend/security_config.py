"""
Security Configuration for E-Commerce Backend
This file contains production-ready security settings.
"""

import os
from decouple import config

# Security Settings for Production
SECURITY_SETTINGS = {
    # HTTPS Settings
    'SECURE_SSL_REDIRECT': config('SECURE_SSL_REDIRECT', default=False, cast=bool),
    'SECURE_HSTS_SECONDS': config('SECURE_HSTS_SECONDS', default=31536000, cast=int),
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    
    # Cookie Security
    'SESSION_COOKIE_SECURE': config('SESSION_COOKIE_SECURE', default=False, cast=bool),
    'CSRF_COOKIE_SECURE': config('CSRF_COOKIE_SECURE', default=False, cast=bool),
    'SESSION_COOKIE_HTTPONLY': True,
    'CSRF_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'Strict',
    'CSRF_COOKIE_SAMESITE': 'Strict',
    
    # Content Security
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'SECURE_BROWSER_XSS_FILTER': True,
    'X_FRAME_OPTIONS': 'DENY',
    
    # Force HTTPS for certain headers
    'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
}

# Additional Security Middleware
SECURITY_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Password Security
PASSWORD_SECURITY = {
    'MIN_LENGTH': 8,
    'REQUIRE_UPPER': True,
    'REQUIRE_LOWER': True,
    'REQUIRE_DIGIT': True,
    'REQUIRE_SPECIAL': True,
}

# Rate Limiting Settings (for future implementation)
RATE_LIMITING = {
    'LOGIN_ATTEMPTS': 5,
    'REGISTRATION_ATTEMPTS': 3,
    'PASSWORD_RESET_ATTEMPTS': 3,
    'API_REQUESTS_PER_MINUTE': 100,
}

# Sensitive Data Protection
SENSITIVE_FIELDS = [
    'password',
    'secret_key',
    'token',
    'api_key',
    'credit_card',
    'ssn',
    'social_security',
]

# Admin Security
ADMIN_SECURITY = {
    'ENABLE_2FA': config('ADMIN_2FA', default=False, cast=bool),
    'SESSION_TIMEOUT': 1800,  # 30 minutes
    'FORCE_PASSWORD_CHANGE': config('FORCE_ADMIN_PASSWORD_CHANGE', default=False, cast=bool),
    'ALLOWED_IPS': config('ADMIN_ALLOWED_IPS', default='', cast=str).split(',') if config('ADMIN_ALLOWED_IPS', default='') else [],
}

# API Security Headers
API_SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
}

# JWT Security Settings
JWT_SECURITY = {
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_LIFETIME_MINUTES': 15,  # Short lived access tokens
    'REFRESH_TOKEN_LIFETIME_DAYS': 7,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

# File Upload Security
FILE_UPLOAD_SECURITY = {
    'MAX_FILE_SIZE': 5 * 1024 * 1024,  # 5MB
    'ALLOWED_EXTENSIONS': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'SCAN_FOR_MALWARE': config('SCAN_UPLOADS', default=False, cast=bool),
    'QUARANTINE_SUSPICIOUS': True,
}

# Database Security
DATABASE_SECURITY = {
    'ENCRYPT_AT_REST': config('DB_ENCRYPTION', default=False, cast=bool),
    'CONNECTION_TIMEOUT': 30,
    'QUERY_TIMEOUT': 300,
    'MAX_CONNECTIONS': 100,
}

# Logging Security Events
SECURITY_LOGGING = {
    'LOG_FAILED_LOGINS': True,
    'LOG_PERMISSION_DENIED': True,
    'LOG_ADMIN_ACTIONS': True,
    'LOG_DATA_CHANGES': True,
    'ALERT_ON_SUSPICIOUS_ACTIVITY': True,
}
