# Django settings for tt project.
# -*- coding: utf-8 -*-

import pprint
import pprint
import os
import socket
import logging
import collections

ALLOWED_HOSTS = ['127.0.0.1']

hostname = socket.gethostname()
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = PROJECT_ROOT + '/static/'
STATIC_ROOT = PROJECT_ROOT + '\\static\\'
# pprint.pprint(STATIC_ROOT)
# exit()
#

print 'hostname type (', type(hostname), hostname, ')'

# exit()

# hostname = 'dmorozov'

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR_ROOT = os.path.join(PROJECT_DIR, '../')

# pprint.pprint(hostname)
# exit()

if hostname == 'dmorozov':
    PROJECT_URL = "http://127.0.0.1:8000/"
# if hostname == 'dm-morozov':
#     PROJECT_URL = "http://127.0.0.1:8000/"
# if hostname == 'njurkin':
#     PROJECT_URL = "http://njurkin:8000/"
# if hostname == "devtt.dmz":
#     PROJECT_URL = 'http://devtt.minsk.ximxim.com/'  # static for nginx
# if hostname == "wwwloc.dmz":
#     Project_URL = 'https://tt.minsk.ximxim.com/'


DEBUG = True
# DEBUG = False

#loging
logging.basicConfig(level=logging.DEBUG, format = '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s', filename=os.path.join(PROJECT_ROOT, 'log/tt_debug.log'), filemode='a+')

# EMAIL_HOST = 'mail.dmz'
EMAIL_HOST = 'mail.example.tst'

TEMPLATE_DEBUG = DEBUG

EMAIL_PORT = 25
# EMAIL_HOST_USER = "myurkin"
# EMAIL_HOST_PASSWORD = "lasto4ka"
EMAIL_HOST_USER = "sarmed"
EMAIL_HOST_PASSWORD = "panda2014"
EMAIL_USE_TLS = True

ADMINS = (
    ('Mikalai Yurkin', 'myurkin@minsk.ximxim.com'),
    # ('Dm Morozov', 'dmorozov@minsk.ximxim.com'),
)

MANAGERS = ADMINS
USE_LOCAL_DB = True


if hostname == "dmorozov":
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'timetracker',                         # Or path to database file if using sqlite3.
        'USER': 'root',                       # Not used with sqlite3.
        'PASSWORD': 'panda2014',                   # Not used with sqlite3.
        # 'HOST': '127.0.0.1',                  # Set to empty string for localhost. Not used with sqlite3.
        # 'PORT': '3306',                       # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUESTS': True,
    }
    }

# if hostname == "dm-morozov":
#     DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'timetracker',                         # Or path to database file if using sqlite3.
#         'USER': 'root',                       # Not used with sqlite3.
#         'PASSWORD': 'panda2014',                   # Not used with sqlite3.
#         # 'HOST': '127.0.0.1',                  # Set to empty string for localhost. Not used with sqlite3.
#         # 'PORT': '3306',                       # Set to empty string for default. Not used with sqlite3.
#     }
#     }
#
#if hostname == "njurkin":
#    DATABASES = {
#	'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'tt',                         # Or path to database file if using sqlite3.
#        'USER': 'root',                       # Not used with sqlite3.
#        'PASSWORD': '1234',                   # Not used with sqlite3.
#        'HOST': '127.0.0.1',                  # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '3306',                       # Set to empty string for default. Not used with sqlite3.
#	}
#}
#
#if hostname == "devtt.dmz":
#    DATABASES = {
#	'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'devtt',                      # Or path to database file if using sqlite3.
#        'USER': 'devttuser',                      # Not used with sqlite3.
#        'PASSWORD': 'JyU3QefESA2EJUw7',                  # Not used with sqlite3.
#        'HOST': 'mysql.dmz',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}
#
#if hostname == "wwwloc.dmz":
#    DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#            'NAME': 'tt', # Or path to database file if using sqlite3.
#            'USER': 'tt', # Not used with sqlite3.
#            'PASSWORD': 'zD5FNdTeJyrGxxaP', # Not used with sqlite3.
#            'HOST': 'mysql.dmz', # Set to empty string for localhost. Not used with sqlite3.
#            'PORT': '', # Set to empty string for default. Not used with sqlite3.
#    }
#}


########################################################
#LDAP AUTH
########################################################

# here we describe LDAP settings as a list of dictionaries, and we can put here just 1 ldap settings or more
AD_LDAP=[
#ldap for BY
#{'LDAP_URL':'ldap://ldap.dmz:389','LDAP_SEARCH_DN':'ou=Users,dc=minsk,dc=ximxim,dc=com'},
{'LDAP_URL':'ldap://192.168.10.3:389','LDAP_SEARCH_DN':'ou=Users,dc=minsk,dc=ximxim,dc=com'},
#ldap for Ulianovsk (RU)
#{'LDAP_URL':'ldap://192.168.4.1:389','LDAP_SEARCH_DN':'ou=people,dc=ximad,dc=com'}
]

#here we describe the set of CSS files that we will apply to our pages on some days (birthdays, holidays, etcs)
EVENTS = {
'02/22':'style23.css',
'02/23':'style23.css',
'02/24':'style23.css',
'03/07':'style8.css',
'03/08':'style8.css',
}
########################################################

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Minsk'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

SESSION_COOKIE_AGE = 604800 #2days

# Absolute filesystem path to the directory that hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
## temporal if hostname == "NC" or hostname == "abogdanovich":

if hostname=='dmorozov':
    MEDIA_URL = 'http://127.0.0.1:8000/media/' #static for django
# if hostname=='dm-morozov':
#     MEDIA_URL = 'http://127.0.0.1:8000/media/' #static for django
# if hostname=='njurkin':
#     MEDIA_URL = 'http://njurkin:8000/media/' #static for django
# if hostname  == "devtt.dmz":
#     MEDIA_URL = 'http://devtt.minsk.ximxim.com/media/' #static for nginx
# if hostname == "wwwloc.dmz":
#     MEDIA_URL ='https://tt.minsk.ximxim.com/media/'


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"

## temporal if hostname == "NC" or hostname == "abogdanovich":
# pprint.pprint(hostname);
# exit()

if hostname=='dmorozov':
    STATIC_URL = 'http://127.0.0.1:8000/static/' #static for django
# if hostname=='dm-morozov':
#     STATIC_URL = 'http://127.0.0.1:8000/static/' #static for django
# if hostname=='njurkin':
#     STATIC_URL = 'http://njurkin:8000/static/' #static for django
# if hostname == "devtt.dmz":
#     STATIC_URL = 'http://devtt.minsk.ximxim.com/static/' #static for nginx
# if hostname == "wwwloc.dmz":
#     STATIC_URL = 'https://tt.minsk.ximxim.com/static/' #static for nginx

#dajaxproject
DAJAXICE_DEBUG = True

DAJAXICE_MEDIA_PREFIX = "dajax"
DAJAXICE_CACHE_CONTROL = 5*24*60*60  #days*hours*min*seconds

############################################

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    #'/sharefs/root/tt/static/',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    # it for admin panel
    "django.contrib.messages.context_processors.messages"
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x^hp325v%#h5h$!db#n*y*j^8raty28co1rh0b2dr#%g2kal52'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    # 'django.template.loaders.filesystem.Loader',
    # 'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.load_template_source',


    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    # "MessageMiddleware"
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware', #need or not?
)


if hostname == "dmorozov":
    ROOT_URLCONF = 'urls'
# if hostname == "dm-morozov":
#     ROOT_URLCONF = 'urls'
# if hostname == "njurkin":
#     ROOT_URLCONF = 'tt.urls'
# if hostname == "devtt.dmz":
#     ROOT_URLCONF = 'devtt.urls'
# if hostname == "wwwloc.dmz":
#     ROOT_URLCONF = 'tt.urls'

TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)


#
# from django_multiuploader_demo.multiuploader.views import *
# from django_multiuploader_demo.multiuploader import *
import django_multiuploader_demo
from django_multiuploader_demo import *


INSTALLED_APPS = (
    # Its for admin panel
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    # [end] Its for admin panel


    'django_multiuploader_demo',
    # 'django_multiuploader_demo.multiuploader',
    # 'django_multiuploader_demo.multiuploader.views',

#    'sorl.thumbnail',
    'easy_thumbnails',


    'django.contrib.sites',
    'django.contrib.staticfiles',
    'timecard',
    'dajaxice',
    'dajax',
    'taggit',
    'taggit_templatetags',
    'django_select2',
    'south',
    'bootstrap',
    'classytags',
    'erp',
    'cv',
    'projects',
    'customers',
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
