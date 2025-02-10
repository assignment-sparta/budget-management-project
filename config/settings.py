from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

# ------------------------------------------------------------------------------
# 애플리케이션 설정 (Application Settings)
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
]

LOCAL_APPS = [
    "budget_management_project.account",
    "budget_management_project.budget",
    "budget_management_project.expense",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.root_urls"

APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------------------------------------
# 데이터베이스 설정 (Database Settings)
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}


# ------------------------------------------------------------------------------
# 국제화 설정 (Internationalization Settings)
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/seoul"

USE_I18N = True

USE_TZ = True


# ------------------------------------------------------------------------------
# 정적 파일 설정 (Static Files Settings)
# ------------------------------------------------------------------------------
STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

# ------------------------------------------------------------------------------
# Django 기타 설정 (Django Miscellaneous Settings)
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "account.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ------------------------------------------------------------------------------
# REST Framework 설정 (REST Framework Settings)
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # JWT
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# ------------------------------------------------------------------------------
# JWT 설정 (JWT Settings)
# ------------------------------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
}


# ------------------------------------------------------------------------------
# Spectacular 설정 (Spectacular Settings)
# ------------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "drf-spectacular API Document",
    "DESCRIPTION": "drf-specatular 를 사용해서 만든 API 문서입니다.",
    "SWAGGER_UI_SETTINGS": {
        "dom_id": "#swagger-ui",
        "layout": "BaseLayout",
        "deepLinking": True,
        "displayOperationId": True,
        "filter": True,
    },
    "LICENSE": {
        "name": "MIT License",
    },
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@3.38.0",
}
