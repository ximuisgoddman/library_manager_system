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

book_path = os.path.abspath(os.path.join(os.getcwd(), "..", "books"))
user_path = os.path.abspath(os.path.join(os.getcwd(), "..", "users"))
sys.path.append(book_path)
sys.path.append(user_path)
from books import views as lib_views
from users import views as user_views
from borrow_record import views as borrow_record_view
from django.contrib import admin

urlpatterns = [
    path('books/', lib_views.book_list, name='book_list'),
    path('books/add/', lib_views.book_create, name='book_create'),
    path('books/<int:book_id>/', lib_views.book_detail, name='book_detail'),
    path('books/<int:book_id>/update/', lib_views.book_update, name='book_update'),
    path('books/<int:book_id>/delete/', lib_views.book_delete, name='book_delete'),
    path('books/<int:book_id>/borrow/', lib_views.book_borrow, name='book_borrow'),
    path("captcha/", include('captcha.urls')),
    path("login/", user_views.my_login, name='login'),
    path("register/", user_views.my_register, name='register'),
    path('logout/', user_views.logout, name='logout'),
    path('borrow_record/', borrow_record_view.borrow_record, name='borrow_record'),
    path('borrow_record_detail/<int:record_id>/', borrow_record_view.borrow_record_detail, name='borrow_record_detail'),
    path('admin/', admin.site.urls)
]
