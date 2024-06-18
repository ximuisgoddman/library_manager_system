"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
import os
import sys
from django.contrib.auth.decorators import login_required
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

import article.views

book_path = os.path.abspath(os.path.join(os.getcwd(), "..", "books"))
user_path = os.path.abspath(os.path.join(os.getcwd(), "..", "users"))

from books import views as book_views
from users import views as user_views
from online_song import views as online_song_view
from online_books import views as online_book_views
from lottery import views as lottery_view
from online_games import views as online_games_view

# from my_blog import views as blog_view
sys.path.append(book_path)
sys.path.append(user_path)

from .admin_front_page_views import user_info_manage_view
from .library_front_page_views import library_front_page_views
from django.contrib import admin

from django.conf.urls.static import static

from django.urls import path, include

from article import views as article_view

import os
from django.http import HttpResponse
import debug_toolbar


def get_host_name(request):
    host_name = os.environ.get('HOSTNAME', 'None')
    info = f'您当前访问的主机是:{host_name}'
    return HttpResponse(info)


urlpatterns = [
    path("say_hello/", get_host_name, name='get_host_name'),
    path("captcha/", include('captcha.urls')),
    path('admin/', admin.site.urls),
    path("login/", user_views.my_login, name='login'),
    path("register/", user_views.my_register, name='register'),
    path('logout/', user_views.logout, name='logout'),
    path('user_edit/<int:user_id>', user_views.user_edit, name='user_edit'),
    path('user_delete/<int:user_id>', user_views.user_delete, name='user_delete'),
    path('follow_user/<int:author_id>/<int:article_id>', article_view.follow_user, name='follow_user'),
    path('my_collect_article_list/<int:user_id>', article_view.my_collect_article_list, name='my_collect_article_list'),
    path('admin_book_list', book_views.admin_book_list, name='admin_book_list'),
    path('books/', book_views.book_front_page, name='book_front_page'),
    path('books/add/', book_views.book_create, name='book_create'),
    path('books/<int:book_id>/', book_views.book_detail, name='book_detail'),
    path('books/<int:book_id>/update/', book_views.book_update, name='book_update'),
    path('books/<int:book_id>/delete/', book_views.book_delete, name='book_delete'),
    path('books/<int:book_id>/borrow/', book_views.book_borrow, name='book_borrow'),
    path('user_books/<int:book_id>/', book_views.user_book_detail, name='user_book_detail'),

    path('user_borrow_record/<int:record_user_id>/', book_views.user_borrow_record, name='user_borrow_record'),
    path('user_borrow_record_detail/<int:record_id>/', book_views.user_borrow_record_detail,
         name='user_borrow_record_detail'),
    path('admin_borrow_record/<int:record_user_id>/', book_views.admin_borrow_record,
         name='admin_borrow_record'),
    path('admin_borrow_record_detail/<int:record_id>/', book_views.admin_borrow_record_detail,
         name='admin_borrow_record_detail'),

    path('online_books/list', online_book_views.admin_online_book_list, name='admin_online_book_list'),
    path('online_books/add/', online_book_views.online_book_create, name='online_book_create'),
    path('online_books/<int:book_id>/', online_book_views.online_book_detail, name='online_book_detail'),
    path('online_books/<int:book_id>/update/', online_book_views.online_book_update, name='online_book_update'),
    path('online_books/<int:book_id>/delete/', online_book_views.online_book_delete, name='online_book_delete'),
    path('online_books/<int:book_id>/add_book_shelf/', online_book_views.add_book_shelf, name='add_book_shelf'),
    path('user_online_book_list/', online_book_views.user_online_book_list, name='user_online_book_list'),
    path('read_online_book/<int:book_id>/', online_book_views.read_online_book, name='read_online_book'),

    path('user_book_shelf_list/<int:book_shelf_user_id>', online_book_views.user_book_shelf_list,
         name='user_book_shelf_list'),
    path('delete_book_shelf/<int:book_id>/', online_book_views.delete_book_shelf,
         name='delete_book_shelf'),

    path('admin_book_shelf_list/<int:book_shelf_user_id>', online_book_views.admin_book_shelf_list,
         name='admin_book_shelf_list'),
    path('admin_book_shelf_detail/<int:record_id>/', online_book_views.admin_book_shelf_detail,
         name='admin_book_shelf_detail'),

    path('book_front_page/', book_views.book_front_page, name='book_front_page'),
    path('online_song_list/', online_song_view.online_song_list, name='online_song_list'),
    path('admin_online_song_list/', online_song_view.admin_online_song_list, name='admin_online_song_list'),
    path("upload_song", online_song_view.upload_song, name='upload_song'),
    path("online_song_update/<int:song_id>/update/", online_song_view.online_song_update, name='online_song_update'),
    path("online_song_delete/<int:song_id>/update/", online_song_view.online_song_delete, name='online_song_delete'),
    path("add_to_favorite", online_song_view.add_to_favorite, name='add_to_favorite'),
    path("my_favorite_music_list/<int:favorite_music_user_id>", online_song_view.my_favorite_music_list,
         name='my_favorite_music_list'),
    path("delete_favorite_music/<int:music_id>/", online_song_view.delete_favorite_music,
         name='delete_favorite_music'),



    path("lottery_view/", lottery_view.lottery_view, name='lottery_view'),
    path("upload_lottery_info/", lottery_view.upload_lottery_info, name='upload_lottery_info'),
    path('users_manage/', user_info_manage_view.users_manage, name='users_manage'),
    path('', library_front_page_views.library_front_page, name='home'),
    path('favicon.ico', RedirectView.as_view(url='/static/ico/favicon.ico')),

    # 重置密码app
    # path('password-reset/', include('password_reset.urls')),
    # 新增代码，配置app的url
    path('article/', include('article.urls', namespace='article')),
    # 评论
    path('comment/', include('comment.urls', namespace='comment')),
    # djang-notifications
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),  # notice
    path('notice/', include('notice.urls', namespace='notice')),
    # django-allauth
    path('accounts/', include('allauth.urls')),

    path('demo/', article.views.demo, name='demo'),
    path("upload/", article.views.upload, name="upload"),
    path("spaceship_shoot/", online_games_view.spaceship_shoot, name="spaceship_shoot"),
    path('pacman/', online_games_view.pacman, name='pacman'),
    path('game2048/', online_games_view.game2048, name='game2048'),
    path('sliding_puzzle/', online_games_view.sliding_puzzle, name='sliding_puzzle'),
    path('super_mario/', online_games_view.super_mario_bros, name='super_mario'),
    path("online_games/", online_games_view.online_games, name='online_games'),

    path("tetris/", online_games_view.tetris, name='tetris'),
    path("snake/", online_games_view.snake, name="snake"),
]
from django.conf import settings

if settings.DEBUG:
    urlpatterns.extend([path('__debug__/', include(debug_toolbar.urls))])

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
