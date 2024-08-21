"""
Django settings for library project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from . import utils

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jtx45ur93nc&)1yd(rc@uuh@*(=e#f1*lp*vp9%+^m5$vh-7xs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.24.96.143', '127.0.0.1', '10.58.237.117', '192.168.1.3', 'django']

# Application definition

INSTALLED_APPS = [
    # 性能分析工具
    'debug_toolbar',
    'lottery',
    'relax_moment',
    'online_song',
    'books',
    'users',
    'online_books',
    'online_games',
    'admin_users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',  # 注册验证码模块,captcha需要在数据库中建立自己的数据表，所以需要执行migrate命令生成数据表
    # Third party apps
    'bootstrap4',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 可添加需要的第三方登录
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.weibo',
    # 'password_reset',
    'taggit',
    'ckeditor',
    'mptt',
    'notifications',
    'article',
    'markdownx',
    'comment',
    'notice',
    'mdeditor',
    'corsheaders',
]

AUTH_USER_MODEL = 'users.MyUser'
MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'library.urls'

# 可以看到debug窗口的ip
INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: False,  # 是否显示工具栏的回调函数
    'SHOW_COLLAPSED': True,  # 是否折叠工具栏的初始状态
    'ENABLE_STACKTRACES': True,  # 是否启用堆栈跟踪面板
    'RESULTS_CACHE_SIZE': 10,  # 缓存的最大查询数量
    'RESULTS_STORE_SIZE': 10,  # 存储的最大查询数量
    'SHOW_TEMPLATE_CONTEXT': True,  # 是否显示模板上下文
    'SHOW_SQL_TOTAL_TIME': True,  # 是否显示 SQL 查询的总时间
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'library.context_processors.user',

            ],
        },
    },
]

WSGI_APPLICATION = 'library.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
            'NAME': os.getenv('MYSQL_DATABASE'),  # 数据库名称
            'HOST': '127.0.0.1',  # 数据库地址，本机 ip 地址 127.0.0.1
            'PORT': '3306',  # 端口
            'USER': 'root',  # 数据库用户名
            'PASSWORD': os.getenv('MYSQL_PASSWORD'),  # 数据库密码
        }
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join("D:/", "temp_files", "log.txt"),
#         },
#     },
#     'loggers': {
#         'myapp': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#         },
#     },
# }

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#     },
# }


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",  # 指定了Redis服务器的位置,如果Redis服务器不在本地主机上，则应使用相应的IP地址或主机名来替换127.0.0.1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "library:",  # 指定缓存键的前缀，以便将缓存键命名空间化
    }
}
BROKER_URL = 'redis://127.0.0.1:6379/0'
# 设置存储结果的后台
RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

USE_CELERY = utils.str_to_bool(os.getenv("USE_CELERY"))
IF_RUN_ON_DOCKER = utils.str_to_bool(os.getenv("IF_RUN_ON_DOCKER"))

if IF_RUN_ON_DOCKER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DATABASE'),
            'USER': 'root',
            'PASSWORD': os.getenv('MYSQL_PASSWORD'),
            'HOST': 'db',
            'PORT': '3306',
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "library:",
        }
    }
    BROKER_URL = 'redis://redis:6379/0'

    # 设置存储结果的后台
    RESULT_BACKEND = 'redis://redis:6379/0'

# 指定Django会话存储的后端和缓存别名
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = [
    # 'django.contrib.auth.backends.ModelBackend',
    'backends.user_backend.UserBackend',
    'backends.admin_user_backend.AdminUserBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_URL = '/login/'

# STATICFILES_DIRS是指定静态文件的目录
# STATIC_ROOT是指定静态文件的收集目录
# MEDIA_ROOT指定了媒体文件的保存目录
# MEDIA_URL指定了媒体文件的URL前缀
# 在这个示例中，静态文件存储在应用目录下的static目录中，媒体文件存储在应用目录下的media目录中
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ADMIN_FRONT_PAGE_VIEWS_DIR = os.path.join(BASE_DIR, 'admin_front_page_views')

CKEDITOR_CONFIGS = {
    # django-ckeditor默认使用default配置
    'default': {
        # 编辑器宽度自适应
        'width': 'auto',
        'height': '250px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            # 表情 代码块
            ['Smiley', 'CodeSnippet'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 链接
            ['Link', 'Unlink'],
            # 列表
            ['NumberedList', 'BulletedList'],
            # 最大化
            ['Maximize']
        ],
        # 插件
        'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils']),
    }
}

# 设置站点
SITE_ID = 1
# 重定向 url
LOGIN_REDIRECT_URL = '/home'
# 可接受的内容格式
accept_content = ["json"]
# 任务序列化数据格式
task_serializer = "json"
# 结果序列化数据格式
result_serializer = "json"
