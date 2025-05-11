from django.utils.translation import gettext_lazy as _
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('uz', _('Uzbek')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale/", "en"),
    os.path.join(BASE_DIR, "locale/", "ru"),
    os.path.join(BASE_DIR, "locale/", "uz"),

]

# cred = credentials.Certificate("config/firebaseaccountkey/serviceAccountKey.json")
# default_app = firebase_admin.initialize_app(cred)

SECRET_KEY = os.getenv("SECRET_KEY", default="foo")

DEBUG = True  # os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = ["*"]


# CSRF_TRUSTED_ORIGINS=*

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_crontab',
    'drf_spectacular',
    'modeltranslation',
    'rosetta',
]


THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_yasg",
    "corsheaders",
]


CUSTOM_APPS = [
    "app",
    "users",
]


INSTALLED_APPS += THIRD_PARTY_APPS + CUSTOM_APPS


SITE_ID = 1


CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',  
    'http://localhost:3000', 
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    'https://carmanagement-1-rmyc.onrender.com/',
    'https://xsoftt.vercel.app'
]

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]


AUTH_USER_MODEL = "users.User"


SERIALIZERS = {
    'USER_SERIALIZER': 'users.serializers.UserSerializer',
}
ROOT_URLCONF = "configs.urls"  


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
                "django.template.context_processors.static",
            ],
        },
    },
]



DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("SQL_DATABASE","demo_fj8x"),
        "USER": os.getenv("SQL_USERNAME","demo_user"),
        "PASSWORD": os.getenv("SQL_PASSWORD","f8wYyZVuLtkDQVBaQmqvSidnb3zcUjT5"),
        "HOST": os.getenv("SQL_HOST", "dpg-d0379egdl3ps739jj3hg-a"),
        "PORT": os.getenv("SQL_PORT", "5432"),
    }
}

# If using Render or another service, override database settings
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES["default"] = dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)

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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Car management',
    'DESCRIPTION': 'Detailed documentation of all API endpoints',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    
    'SECURITY': [
        {
            'Bearer': [],
        }
    ],
    'AUTHENTICATION_WHITELIST': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # Token expires in 15 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # Refresh token expires in 1 day
    'ROTATE_REFRESH_TOKENS': False,  # Generates new refresh token on use
    'BLACKLIST_AFTER_ROTATION': True,  # Blacklist old refresh tokens
    'ALGORITHM': 'HS256',  # Default hashing algorithm
    'SIGNING_KEY': SECRET_KEY,  # Uses Django's SECRET_KEY
    'AUTH_HEADER_TYPES': ('Bearer',),  # Authorization: Bearer <token>
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# Load local settings if available
try:
    from local_settings import *
except ImportError:
    pass