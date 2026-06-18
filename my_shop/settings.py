import os
from pathlib import Path
import dj_database_url

# ይህ BASE_DIR የፕሮጀክትህን ዋና ማህደር በትክክል መለየት አለበት
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-ra0v(_u4nm7s*4paat87t4#i8d3j%j_5osi8bbp$-+gdwl*+ia')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['my-shop-jljx.onrender.com', 'localhost', '127.0.0.1', '*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ለStatic ፋይሎች አስፈላጊ ነው
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
        # አሁን የ templates ማህደርህ ከ manage.py ጋር በአንድ ደረጃ (Root) ላይ ነው
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

# የDatabase ግንኙነት
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR}/db.sqlite3',
        conn_max_age=600,
        ssl_require=True # Render ላይ ለPostgreSQL አስፈላጊ ነው
    )
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'am'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# የLogin መዳረሻዎች
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'

LANGUAGES = [('en', 'English'), ('am', 'አማርኛ')]
LOCALE_PATHS = [BASE_DIR / 'locale']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'