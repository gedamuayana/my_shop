import os
from pathlib import Path
import dj_database_url

# BASE_DIR መገኛ
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY - በRender Environment Variables ላይ ቢቀመጥ ይመረጣል
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-ra0v(_u4nm7s*4paat87t4#i8d3j%j_5osi8bbp$-+gdwl*+ia')

# DEBUG ቅንብር - Production ላይ False መሆን አለበት
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['my-shop-jljx.onrender.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic', # WhiteNoise በልማት ጊዜም እንዲሰራ
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Static ፋይሎችን ለማገልገል
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_shop.urls'

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

WSGI_APPLICATION = 'my_shop.wsgi.application'

# የዳታቤዝ ማዋቀር
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Login Redirects
LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'

# Static Files ማዋቀር (Render ለዲዛይን አስፈላጊ ነው)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static'] # የአንተ static አቃፊ ካለህ
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files ማዋቀር
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ቋንቋ እና ሰዓት
LANGUAGE_CODE = 'am'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [('en', 'English'), ('am', 'አማርኛ')]
LOCALE_PATHS = [BASE_DIR / 'locale']