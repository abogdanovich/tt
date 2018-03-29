# Django settings for tt project.
# -*- coding: utf-8 -*-

import os, sys
import socket
import logging

hostname = socket.gethostname()

PROJECT_ROOT= os.path.realpath(os.path.dirname(__file__))
DEBUG = False

#loging    
logging.basicConfig(level=logging.DEBUG, format = '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s', filename=os.path.join(PROJECT_ROOT, 'log/tt_debug.log'), filemode='a+')

if hostname == "NC" or hostname == "abogdanovich" or hostname == "dmorozov":
    DEBUG = True
    EMAIL_HOST = 'mail.minsk.ximxim.com'

else:
    EMAIL_HOST = 'mail.dmz'
    
TEMPLATE_DEBUG = DEBUG

EMAIL_PORT = 25
# EMAIL_HOST_USER = "abogdanovich"
EMAIL_HOST_USER = "dmorozov"

EMAIL_HOST_PASSWORD = "sensorium"
EMAIL_USE_TLS = True

ADMINS = (
    ('Alex Bogdanovich', 'abogdanovich@minsk.ximxim.com'),
)

MANAGERS = ADMINS

if hostname == "NC" or hostname == "abogdanovich" or hostname == "dmorozov":
    DATABASES = {
	'default': {
        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tt',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'panda2014',                  # Not used with sqlite3.
        'HOST': '/opt/lampp/var/mysql/mysql.sock',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
	}
    }

else:
    DATABASES = {
	'default': {
        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tt',                      # Or path to database file if using sqlite3.
        'USER': 'tt',                      # Not used with sqlite3.
        'PASSWORD': 'zD5FNdTeJyrGxxaP',                  # Not used with sqlite3.
        'HOST': 'mysql.dmz',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
	}
    }


########################################################
#LDAP AUTH
########################################################

AD_DNS_NAME = 'ldap.dmz'
AD_LDAP_PORT = 389
AD_SEARCH_DN = 'ou=Users,dc=minsk,dc=ximxim,dc=com'
AD_SEARCH_DN_GROUP = 'ou=Users,dc=minsk,dc=ximxim,dc=com'
AD_NT4_DOMAIN = ''
AD_LDAP_URL = 'ldap://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)


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
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
if hostname == "NC" or hostname == "abogdanovich" or hostname == "dmorozov":
    MEDIA_URL = 'http://127.0.0.1:8000/media/' #static for django
else:
    MEDIA_URL = 'https://tt.minsk.ximxim.com/media/' #static for nginx


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"

if hostname == "NC" or hostname == "abogdanovich" or hostname == "dmorozov":
    STATIC_URL = 'http://127.0.0.1:8000/static/' #static for django
else:
    STATIC_URL = 'https://tt.minsk.ximxim.com/static/' #static for nginx

############################################
#dajaxproject
DAJAXICE_DEBUG = False

DAJAXICE_MEDIA_PREFIX = "dajax"
DAJAXICE_CACHE_CONTROL = 5*24*60*60 #days*hours*min*seconds

DAJAXICE_FUNCTIONS = (
	'timecard.ajax.save_user_settings',
	'timecard.ajax.send_time_correction',
	'timecard.ajax.set_day_off',
	'timecard.ajax.save_user_avatar',
	'timecard.ajax.show_user_details',
	'timecard.ajax.user_image_rotate',
	'timecard.ajax.user_image_filters',
	'timecard.ajax.save_user_time',
	'timecard.ajax.save_spam_comment',
	'timecard.ajax.user_change_mod',
	'timecard.ajax.add_new_user',
	'timecard.ajax.show_correct_dialog',
	'timecard.ajax.approve_corrected_time',
	'timecard.ajax.make_root',
	'timecard.ajax.make_admin',
	'timecard.ajax.make_boss',
	'timecard.ajax.make_user',
	'timecard.ajax.delete_record',
	'timecard.ajax.add_corrected_time',
	'timecard.ajax.delete_spam_post',
	'timecard.ajax.delete_spam_comment',
	'timecard.ajax.change_user_dep',
	'timecard.ajax.show_boss_notice',
	'timecard.ajax.save_boss_notice',
	'timecard.ajax.save_duty_date',
	'timecard.ajax.add_report_project',
	
)

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
    "django.contrib.messages.context_processors.messages"
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x^hp325v%#h5h$!db#n*y*j^8raty28co1rh0b2dr#%g2kal52'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
)

ROOT_URLCONF = 'tt.urls'

TEMPLATE_DIRS = ( os.path.join(PROJECT_ROOT, 'templates'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.admin',
    'tt.timecard',
    'dajaxice', 
    'dajax', 
    # Uncomment the next line to enable admin documentation:
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
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
