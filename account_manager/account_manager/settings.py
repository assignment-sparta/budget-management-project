from pathlib import Path
from datetime import timedelta # JWT

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w8g_+)od@hs1evu3+t12a5i-)+z4u*zj&exlic)ktyp14$e=+9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# ------------------------------------------------------------------------------
# 애플리케이션 설정 (Application Settings)
# ------------------------------------------------------------------------------
#장고 기본앱
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]

# 서드파티 앱
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular', # drf-spectacular을 사용하여 API 문서를 자동으로 생성하기 위해 추가함
]

# 마이 앱
MY_APPS = [    
    'account',
    'budget',
    'expense',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + MY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'account_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'account_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#유저모델 설정
AUTH_USER_MODEL = 'accounts.User'


REST_FRAMEWORK = {
    # 모든 API에 인증을 필수로 하는 전역 설정

    #API뷰에 인증된 사용자만 접근이 가능한 설정
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  
    ),
    #API 인증 방식을 JWT으로 사용하기로 설정
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication', # JWT
    ),

    # DRF 기본 스키마 클래스를 drf-spectacular의 AutoSchema로 설정
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
}

# 토큰 재사용 방지 JWT 설정
SIMPLE_JWT = {
    # Access Token의 유효 기간 설정
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    # Access Token의 유효 기간 설정
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # Refresh Token 사용 시 새 토큰 발급 여부 설정
    'ROTATE_REFRESH_TOKENS': True,
    # 새 Refresh Token 발급 시 기존 Token을 블랙리스트에 등록
    'BLACKLIST_AFTER_ROTATION': True,
}


# 캐시 처리 고려


# Spectacular 세팅
SPECTACULAR_SETTINGS = {
    # General schema metadata. Refer to spec for valid inputs
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    'TITLE': 'drf-spectacular API Document', # API 문서 이름
    'DESCRIPTION': 'drf-specatular 를 사용해서 만든 API 문서입니다.', 
    'SWAGGER_UI_SETTINGS': {
        'dom_id': '#swagger-ui',
        'layout': 'BaseLayout', 
        'deepLinking': True,  
        'displayOperationId': True,
        'filter': True,
    },
   
    'LICENSE': {
        'name': 'MIT License',
    },
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    'SWAGGER_UI_DIST': '//unpkg.com/swagger-ui-dist@3.38.0',
}