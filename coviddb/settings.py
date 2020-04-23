"""
Django settings for coviddb project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import coviddb

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3-i$$&*acq*+ltusm4(fft7q=+e!-*8-lc8muuf_z+^x55e*ra'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ALLOWED_HOSTS = ['127.0.0.1', 'covid19db.info']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'coviddb',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coviddb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'coviddb.context_processors.age_list',
                'coviddb.context_processors.chart_color',
            ],
        },
    },
]

WSGI_APPLICATION = 'coviddb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, "static"),
)

DB_PATH = 'db.sqlite3'
INFECTED_LIST_TABLE_NAME = "coviddb_infectedperson"

INFECTED_LIST_COLUMN_NAME = [
    'state','pat_id','city_no',
    'announce_date','infected_date','living_state','living_city','age',
    'sex','status','symptoms','occupation','close_contact','rel_close_contact',
    'travel_history','travel_destination','remarks','cluster_location','cluster_name','discharge','death','death_date','full_presentation']

INFECTED_LIST_HEADER_NAME = [
    '発表都道府県','ID番号','全国地方公共団体コード',
    '公表_年月日','発症_年月日','患者_居住地','居住市町村','年代',
    '性別','状態','症状','職業','濃厚接触者','濃厚接触者との関係',
    '渡航歴の有無','渡航場所','備考','クラスタ種別','クラスタ場所','退院済フラグ','死亡','死亡日時','発表全文']

INFECTED_LIST_SIMPLE_COLUMN_INDEX = [0, 1, 3, 4, 6, 7, 8, 9, 10, 11, 12]
INFECTED_LIST_COLUMN_INDEX = INFECTED_LIST_HEADER_NAME[0:2]
INFECTED_LIST_HEADER_DICT = dict(zip(INFECTED_LIST_COLUMN_NAME, INFECTED_LIST_HEADER_NAME))

SEX_DIC = {
    0:'男性',
    1:'女性',
    2:'不明',
}

AREA_DIC = {
    '関東': ['tokyo'],
    '近畿': ['osaka'],
}

INFECTED_NUM_HEADER_NAME = ['都道府県', '感染者数', '入院者数', '退院者数', '死亡者数']

AGE_LIST = ['10歳未満', '10代', '20代', '30代', '40代', '50代', '60代', '70代', '80代', '90代', ]

CHART_COLOR = ['255, 0, 0', '255, 165, 0', '50, 205, 50', '0, 255, 255', '30, 144, 255', '221, 160, 221', '75, 0, 130', '218, 165, 32', '128, 0, 0',
                  '128, 128, 128']