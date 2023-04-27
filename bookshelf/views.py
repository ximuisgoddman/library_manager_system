from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .book_shelf_form import BookShelfForm
from .models import BookShelfModel
from users.models import MyUser


@login_required
def user_book_shelf_list(request, book_shelf_user_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    print("book_shelf_user_id:", book_shelf_user_id, isinstance(book_shelf_user_id, MyUser))
    bookshelfs = BookShelfModel.objects.filter(book_shelf_user_id=book_shelf_user_id)
    return render(request, 'book_shelf/user_book_shelf/user_book_shelf_list.html', {'bookshelfs': bookshelfs})


@login_required
def user_book_shelf_detail(request, record_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    try:
        bookshelf = get_object_or_404(BookShelfModel, id=record_id)
    except Exception as e:
        print("加入书架失败", e)
    else:
        return render(request, 'book_shelf/user_book_shelf/user_book_shelf_detail.html', {'bookshelf': bookshelf})


@login_required
def admin_book_shelf_list(request, book_shelf_user_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    print("book_shelf_user_id:", book_shelf_user_id, isinstance(book_shelf_user_id, MyUser))
    bookshelfs = BookShelfModel.objects.filter(book_shelf_user_id=book_shelf_user_id)
    return render(request, 'book_shelf/admin_book_shelf/admin_book_shelf_list.html', {'bookshelfs': bookshelfs})


@login_required
def admin_book_shelf_detail(request, record_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    try:
        bookshelf = get_object_or_404(BookShelfModel, id=record_id)
    except Exception as e:
        print("加入书架失败", e)
    else:
        return render(request, 'book_shelf/admin_book_shelf/admin_book_shelf_detail.html', {'bookshelf': bookshelf})
