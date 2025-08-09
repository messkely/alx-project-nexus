from pathlib import Path
from decouple import config, Csv
from .security_config import SECURITY_SETTINGS, JWT_SECURITY

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production-with-50-plus-random-characters-including-symbols')

# Security: Only allow specific hosts in production
if DEBUG:
    ALLOWED_HOSTS = ['*']  # Only for development
else:
    allowed_hosts_str = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,testserver,ecom-backend.store,98.87.47.179')
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECURE_SSL_REDIRECT = SECURITY_SETTINGS['SECURE_SSL_REDIRECT']
SECURE_HSTS_SECONDS = SECURITY_SETTINGS['SECURE_HSTS_SECONDS']
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURITY_SETTINGS['SECURE_HSTS_INCLUDE_SUBDOMAINS']
SECURE_HSTS_PRELOAD = SECURITY_SETTINGS['SECURE_HSTS_PRELOAD']
SESSION_COOKIE_SECURE = SECURITY_SETTINGS['SESSION_COOKIE_SECURE']
CSRF_COOKIE_SECURE = SECURITY_SETTINGS['CSRF_COOKIE_SECURE']
SESSION_COOKIE_HTTPONLY = SECURITY_SETTINGS['SESSION_COOKIE_HTTPONLY']
CSRF_COOKIE_HTTPONLY = SECURITY_SETTINGS['CSRF_COOKIE_HTTPONLY']
SESSION_COOKIE_SAMESITE = SECURITY_SETTINGS['SESSION_COOKIE_SAMESITE']
CSRF_COOKIE_SAMESITE = SECURITY_SETTINGS['CSRF_COOKIE_SAMESITE']
SECURE_CONTENT_TYPE_NOSNIFF = SECURITY_SETTINGS['SECURE_CONTENT_TYPE_NOSNIFF']
SECURE_BROWSER_XSS_FILTER = SECURITY_SETTINGS['SECURE_BROWSER_XSS_FILTER']
X_FRAME_OPTIONS = SECURITY_SETTINGS['X_FRAME_OPTIONS']

# Session Security
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	
    # third-party apps
    'corsheaders',  # CORS handling for API requests
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_yasg', # swagger package
    'django_filters',  # Fixed: should be django_filters not django_filters

    # my apps
	'catalog',
    'users',
    'orders',
    'cart',
    'reviews',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at the top
    'django.middleware.security.SecurityMiddleware',
    'ecommerce_backend.security_middleware.SecurityHeadersMiddleware',
    'ecommerce_backend.security_middleware.RateLimitMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'ecommerce_backend.security_middleware.AdminIPWhitelistMiddleware',
    'ecommerce_backend.security_middleware.SecurityLoggingMiddleware',
    'ecommerce_backend.security_middleware.FileUploadSecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

import dj_database_url

# Use DATABASE_URL if available (Docker/Heroku), otherwise fall back to individual settings
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL and DATABASE_URL.strip():
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Fallback for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='ecommerce'),
            'USER': config('DB_USER', default='ecommerce_user'),
            'PASSWORD': config('DB_PASSWORD', default='ecommerce_pass'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# Redis Cache Configuration
REDIS_URL = config('REDIS_URL', default=None)

if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    # Fallback to database sessions
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }




# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files security
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File Upload Security
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
FILE_UPLOAD_PERMISSIONS = 0o644

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# REST Framework Security Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=JWT_SECURITY['ACCESS_TOKEN_LIFETIME_MINUTES']),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=JWT_SECURITY['REFRESH_TOKEN_LIFETIME_DAYS']),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ALGORITHM": JWT_SECURITY['ALGORITHM'],
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": JWT_SECURITY['BLACKLIST_AFTER_ROTATION'],
    "UPDATE_LAST_LOGIN": JWT_SECURITY['UPDATE_LAST_LOGIN'],
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SERIALIZERS': {},
	"PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
}

# Email settings (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@ecommerce.com'

# Frontend URL for password reset (you can change this to your frontend URL)
FRONTEND_URL = 'http://localhost:3000'

# Pagination settings
REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'rest_framework.pagination.PageNumberPagination'
REST_FRAMEWORK['PAGE_SIZE'] = 20

# Rate Limiting
RATE_LIMIT_ENABLED = config('RATE_LIMIT_ENABLED', default=True, cast=bool)

# Admin Security
admin_ips_str = config('ADMIN_ALLOWED_IPS', default='')
ADMIN_ALLOWED_IPS = [ip.strip() for ip in admin_ips_str.split(',') if ip.strip()] if admin_ips_str else []

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'ecommerce_backend.security_middleware': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
import os
logs_dir = BASE_DIR / 'logs'
if not logs_dir.exists():
    os.makedirs(logs_dir, exist_ok=True)

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "https://ecom-backend.store",
    "http://localhost:3000",  # For local frontend development
    "http://127.0.0.1:3000",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.ecom-backend\.store$",  # Allow subdomains
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# For development only - remove in production
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

