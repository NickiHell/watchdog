from typing import Dict, List, Tuple, Union

from django.utils.translation import gettext_lazy as _
from server.settings.components import BASE_DIR, config

SECRET_KEY = config('DJANGO_SECRET_KEY')

AUTH_USER_MODEL = 'users.User'

# Application definition:

INSTALLED_APPS: Tuple[str, ...] = (
    # Your apps go here:
    'watchdog-backend.apps.core',
    'watchdog-backend.apps.users',
    'watchdog-backend.apps.bots',
    'watchdog-backend.apps.nets',
    'watchdog-backend.apps.api',
    'drf_spectacular',
    # Default django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # django-admin:
    'django.contrib.admin',
    'django.contrib.admindocs',
    # Security:
    'axes',
    # Health checks:
    # You may want to enable other checks as well,
    # see: https://github.com/KristianOellegaard/django-health-check
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'django_loguru',
)

MIDDLEWARE: Tuple[str, ...] = (
    # Content Security Policy:
    'csp.middleware.CSPMiddleware',
    # Django:
    'django.middleware.security.SecurityMiddleware',
    # django-permissions-policy
    'django_permissions_policy.PermissionsPolicyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Axes:
    'axes.middleware.AxesMiddleware',
    # Django HTTP Referrer Policy:
    'django_http_referrer_policy.middleware.ReferrerPolicyMiddleware',
    'django_loguru.middleware.DjangoLoguruMiddleware',
)

ROOT_URLCONF = 'watchdog-backend.urls'

ASGI_APPLICATION = 'watchdog-backend.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('DJANGO_DATABASE_HOST'),
        'PORT': config('DJANGO_DATABASE_PORT', cast=int),
        'CONN_MAX_AGE': config('CONN_MAX_AGE', cast=int, default=60),
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=15000ms',
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True
USE_L10N = True

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

USE_TZ = True
TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

_COLLECTSTATIC_DRYRUN = config(
    'DJANGO_COLLECTSTATIC_DRYRUN',
    cast=bool,
    default=False,
)

STATIC_ROOT = 'static' if _COLLECTSTATIC_DRYRUN else '/var/www/django/static'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Templates
# https://docs.djangoproject.com/en/3.2/ref/templates/api

TEMPLATES = [
    {
        'APP_DIRS': True,
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Contains plain text templates, like `robots.txt`:
            BASE_DIR.joinpath('watchdog-backend', 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                # Default template context processors:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    }
]

# Media files
# Media root dir is commonly changed in production
# (see development.py and production.py).
# https://docs.djangoproject.com/en/3.2/topics/files/

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

# Django authentication linux
# https://docs.djangoproject.com/en/3.2/topics/auth/

AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# Security
# https://docs.djangoproject.com/en/3.2/topics/security/

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

# https://github.com/DmytroLitvinov/django-http-referrer-policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
REFERRER_POLICY = 'same-origin'

# https://github.com/adamchainz/django-permissions-policy#setting
PERMISSIONS_POLICY: Dict[str, Union[str, List[str]]] = {}  # noqa: WPS234

# Timeouts
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-EMAIL_TIMEOUT

EMAIL_TIMEOUT = 5

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# DRF-SPECTACULAR
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
}