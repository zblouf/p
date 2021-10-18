from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GENERISQUE_V1_DATAPATH = os.path.join(BASE_DIR, "v1data")

PLATEFORM_NAME = '[Nom de la plateforme]'
COPYRIGHT = '&copy; 2006-2016'

ACCOUNT_DATA_DIR = os.path.join(BASE_DIR, 'data', 'account_media')
ACCOUNT_DATA_ROOT = os.path.join(BASE_DIR, 'data', 'account_media')

DEFAULT_BASE_TEMPLATE = 'main/base.html'

SUPERADMIN_BASE_URL = '/_admin/'
RETAILER_BASE_URL = '/_retail/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#tt3z5=6+&won8+^hxp2p%$v63q8u(6!-5r*2smdct-c2tvn&2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = '/auth/login'
LOGIN_EXEMPT_URLS = (
    r'^auth/',
    r'^help/',
    r'^i18n/',
    r'^media/',
    r'^admin/',
    r'^_admin/',
    r'^_retail/',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap3',
    'django_extensions',
    'reversion',

    'z.meta.option',
    'z.meta.idtag',
    'z.core.main',
    'z.core.app',
    'z.core.logo',
    'z.doc.file',
    'z.doc.link',
    'z.auth.zuser',
    'z.auth.acl',
    'z.org.entity',
    'z.org.hr',
    'z.prev.activity',
    'z.prev.domain',
    'z.prev.hazard',
    'z.prev.action',
    'z.prev.profile',
    'z.prev.assess',
    'z.prev.assess.v1',
    'z.means',
    'z.means.equipment',
    'z.retail.vendor',
#    'z.retail.entity',
    'z.saas',
    'z.superadmin',


)

MIDDLEWARE_CLASSES = (
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'z.core.middleware.TimerMiddleware',

#    'z.auth.middleware.LoginRequiredMiddleware',
    'z.core.middleware.ACLMiddleware',
)

ROOT_URLCONF = 'p.urls'

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

                'z.core.context_processors.z_context',
                'z.core.context_processors.base_template',
            ],
        },
    },
]

WSGI_APPLICATION = 'p.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
MODELTRANSLATION_DEFAULT_LANGUAGE = 'fr'
MODELTRANSLATION_FALLBACK_LANGUAGES = ('fr', 'en')
LANGUAGES = (
    ('fr', _('French')),
    ('en', _('English')),
#    ('de', _('German')),
#    ('es', _('Spanish')),
#    ('it', _('Italian')),
#    ('pt', _('Portuguese')),
#    ('pl', _('Polish')),
#    ('el', _('Greek')),
#    ('ru', _('Russian')),
#    ('eo', _('Esperanto')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# local settings
try:
    from p.local_settings import *
except ImportError:
    print("No local settings found.")
