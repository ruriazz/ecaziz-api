# TODO: core.settings
from pathlib import Path
from .variables import app_config
from .dbconf import db_config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = app_config.get('secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = app_config.get('is_debug')

ALLOWED_HOSTS = app_config.get('allowed_hosts')

# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

APPLICATIONS = [
    'applications.ucapan.apps.UcapanConfig',
    'applications.undangan.apps.UndanganConfig',
    'applications.users.apps.UsersConfig',
]

INSTALLED_APPS =  BASE_APPS + APPLICATIONS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.utils.handlers.custom_exception',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOWED_ORIGINS = app_config.get('allowed_origins')

CORS_ALLOW_HEADERS = [
    'Authorization',
    'X-Requested-With',
    'Content-Type'
]

CSRF_TRUSTED_ORIGINS = app_config.get('trusted_origins')

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', 
#        'NAME': app_config.get('db_name'),
#        'USER': app_config.get('db_user'),
#        'PASSWORD': app_config.get('db_pass'),
#        'HOST': app_config.get('db_host'),
#        'PORT': app_config.get('db_post'),
#    }
# }

DATABASES = {
    'default': {
        'NAME': db_config.get('name'),
        'ENGINE': 'mysql.connector.django',
        'USER': db_config.get('user'),
        'PASSWORD': db_config.get('password'),
        'OPTIONS': {
            'autocommit': True,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_COOKIE_SECURE = True

# CSRF_COOKIE_HTTPONLY = True

# SESSION_COOKIE_SECURE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMIN_ENABLED = app_config.get('admin_enabled')
