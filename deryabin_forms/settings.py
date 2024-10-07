import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1']

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # GRAPPELLI ADMIN
    "grappelli",
    # DJANGO CONTRIB
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    'business_forms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'business_forms.middleware.TelegramAlertMiddleware',
]

ROOT_URLCONF = 'deryabin_forms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'deryabin_forms.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get('DB_NAME'),
        "USER": os.environ.get('DB_USER'),
        "PASSWORD": os.environ.get('DB_PASSWORD'),
        "HOST": os.environ.get('DB_HOST'),
        "PORT": os.environ.get('DB_PORT'),
    }
}

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

LANGUAGE_CODE = 'ru'
LANGUAGES = (("ru", "Russian"),)

TIME_ZONE = 'Europe/Moscow'
USE_I18N = False
USE_L10N = True
USE_TZ = True

# STATIC
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = 'staticfiles'

# MEDIA
MEDIA_URL = 'media/'
MEDIA_DIRS = [
    BASE_DIR / 'media'
]
MEDIA_ROOT = 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

ADMIN_TITLE = GRAPPELLI_ADMIN_TITLE = 'DERYABIN FORMS'

SALEBOT_API_URL = f"https://chatter.salebot.pro/api/{os.environ.get('SALEBOT_API_KEY')}/callback"

MAIN_ADMIN_ID = os.environ.get("MAIN_ADMIN_ID")
ADMINS_CHAT_ID = os.environ.get("ADMINS_CHAT_ID")
TEST_ADMIN_ID = os.environ.get("TEST_ADMIN_ID")

ALERT_CHAT_ID = os.environ.get("ALERT_CHAT_ID")

# BOT CONFIG
BOT_TOKEN = os.getenv('BOT_TOKEN')
TEST_TOKEN = os.getenv('TEST_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
