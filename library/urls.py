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

book_path = os.path.abspath(os.path.join(os.getcwd(), "..", "books"))
user_path = os.path.abspath(os.path.join(os.getcwd(), "..", "users"))

from books import views as lib_views
from users import views as user_views
from borrow_record import views as borrow_record_view

from online_books import views as online_views
from bookshelf import views as bookshelf_views
from django.conf import settings
from django.conf.urls.static import static

sys.path.append(book_path)
sys.path.append(user_path)

from .admin_front_page_views import user_info_manage_view
from .library_front_page_views import library_front_page_views

urlpatterns = [

    path("captcha/", include('captcha.urls')),
    path('admin/', admin.site.urls),
    path("login/", user_views.my_login, name='login'),
    path("register/", user_views.my_register, name='register'),
    path('logout/', user_views.logout, name='logout'),

    path('books/list', lib_views.book_list, name='book_list'),
    path('books/', lib_views.book_front_page, name='book_front_page'),
    path('books/add/', lib_views.book_create, name='book_create'),
    path('books/<int:book_id>/', lib_views.book_detail, name='book_detail'),
    path('books/<int:book_id>/update/', lib_views.book_update, name='book_update'),
    path('books/<int:book_id>/delete/', lib_views.book_delete, name='book_delete'),
    path('books/<int:book_id>/borrow/', lib_views.book_borrow, name='book_borrow'),

    path('user_borrow_record/<int:record_user_id>/', borrow_record_view.user_borrow_record, name='user_borrow_record'),
    path('user_borrow_record_detail/<int:record_id>/', borrow_record_view.user_borrow_record_detail,
         name='user_borrow_record_detail'),
    path('admin_borrow_record/<int:record_user_id>/', borrow_record_view.admin_borrow_record,
         name='admin_borrow_record'),
    path('admin_borrow_record_detail/<int:record_id>/', borrow_record_view.admin_borrow_record_detail,
         name='admin_borrow_record_detail'),

    path('online_books/list', online_views.admin_online_book_list, name='admin_online_book_list'),
    path('online_books/add/', online_views.online_book_create, name='online_book_create'),

    path('online_books/<int:book_id>/', online_views.online_book_detail, name='online_book_detail'),
    path('online_books/<int:book_id>/update/', online_views.online_book_update, name='online_book_update'),
    path('online_books/<int:book_id>/delete/', online_views.online_book_delete, name='online_book_delete'),
    path('online_books/<int:book_id>/add_book_shelf/', online_views.add_book_shelf, name='add_book_shelf'),

    path('user_book_shelf_list/<int:book_shelf_user_id>', bookshelf_views.user_book_shelf_list,
         name='user_book_shelf_list'),
    path('user_book_shelf_detail/<int:record_id>/', bookshelf_views.user_book_shelf_detail,
         name='user_book_shelf_detail'),

    path('admin_book_shelf_list/<int:book_shelf_user_id>', bookshelf_views.admin_book_shelf_list,
         name='admin_book_shelf_list'),
    path('admin_book_shelf_detail/<int:record_id>/', bookshelf_views.admin_book_shelf_detail,
         name='admin_book_shelf_detail'),
    path('user_online_book_list/', online_views.user_online_book_list, name='user_online_book_list'),

    path('book_front_page/', lib_views.book_front_page, name='book_front_page'),

    path('users_manage/', user_info_manage_view.users_manage, name='users_manage'),
    path('library_front_page', library_front_page_views.library_front_page, name='library_front_page')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
