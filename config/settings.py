import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# SÉCURITÉ
# ========================

SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-secret-key")

DEBUG = False  # IMPORTANT pour Vercel

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".vercel.app"
]

# ========================
# APPLICATIONS
# ========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # tes apps
    'app',
    'chatbot',
    'core',
]

# ========================
# MIDDLEWARE
# ========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # 👇 AJOUT IMPORTANT
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ========================
# URLS & WSGI
# ========================

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ========================
# TEMPLATES
# ========================

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

# ========================
# BASE DE DONNÉES
# ========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ⚠️ Plus tard → remplacer par Postgres (recommandé)

# ========================
# VALIDATION PASSWORD
# ========================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================
# INTERNATIONALISATION
# ========================

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========================
# FICHIERS STATIQUES
# ========================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 👇 IMPORTANT POUR VERCEL
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ========================
# DEFAULT PK
# ========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'