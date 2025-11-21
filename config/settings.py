from pathlib import Path
from datetime import timedelta
import os

from pathlib import Path
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%z)*4xzy$$$_o^31#8es5_dncjlu*ygo%$3$s0-yn_z7aat5j3"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["https://globeup-international.onrender.com","*"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "https://amazon-up-v1.netlify.app",
    # add your frontend URLs here
    
    "https://globeup-international.onrender.com"
]
CORS_ALLOW_CREDENTIALS = True



CSRF_TRUSTED_ORIGINS = ['https://globeup-international.onrender.com','https://*.127.0.0.1']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "rest_framework_simplejwt",
    "phonenumber_field",
    "corsheaders",
    # custom apps
    "user",
    "order",
    "ip_block",
    "cart",
    "wishlist",
    "review",
    'fraud_api',
    "category",
    "brand",
    "product",
    "contact",
    "shipping_charge",
    "site_setting",
    # "settings",
    "banner",
    "smtp_mail",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # "config.middleware.ip_block_middleware.IPBlockMiddleware"
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Database configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'globeup',        # Your database name from Render
#         'USER': 'globeup_user',   # Your database user from Render
#         'PASSWORD': 'IMBcN9kb4H3huPBNTic258DLTviAMLpl',  # Your database password from Render
#         'HOST': 'dpg-cv5t6i6n6p6s73d2f5v0-a.oregon-postgres.render.com',  # Your Render host
#         'PORT': '5432',
#         'OPTIONS': {
#             'sslmode': 'require',  # Render requires SSL connections
#         },
#     }
# }



# # Database configuration
# DATABASES = {
#     'default': dj_database_url.config(
#         default= "postgresql://globe_up_aryt_user:OM2gTLwDX1TeiAWJY8ypegTtvJHbw03R@dpg-d2nu84bipnbc73cv885g-a.singapore-postgres.render.com/globe_up_aryt",
#         conn_max_age=600,
#         ssl_require=True
#     )
# }




# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "user.User"


# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # 'rest_framework.authentication.TokenAuthentication',
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,  # Show 10 orders per page

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',  # <-- needed for FormData
    ]
}

# Djoser settings
DJOSER = {
    "USER_ID_FIELD": "id",
    "LOGIN_FIELD": "phone_number",
    "SERIALIZERS": {
        "user_create": "user.serializers.UserCreateSerializer",
        "user": "user.serializers.UserSerializer",
        "current_user": "user.serializers.UserSerializer",
    },
    #  "EMAIL": {
    #     # "password_reset": "emails.CustomPasswordResetEmail",  # relative to app's templates folder
    #     "password_reset": "email/password_reset.html",  # relative to app's templates folder
    # }
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}/",
    "SEND_ACTIVATION_EMAIL": False,
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),  # Default is 5 minutes
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # Default is 1 day
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
}


# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "antoneozaka724@gmail.com"
EMAIL_HOST_PASSWORD = "jlwt bypq tgjq rboi"
DEFAULT_FROM_EMAIL = "GlobeUp <antoneozaka724@gmail.com>"


# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = BASE_DIR / "sent_emails"


# At the bottom of settings.py
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"



