from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .book_shelf_form import BookShelfForm
from .models import BookShelfModel
from users.models import MyUser


@login_required
def book_shelf_list(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    bookshelfs = BookShelfModel.objects.all()
    return render(request, 'book_shelf/book_shelf_list.html', {'bookshelfs': bookshelfs})


@login_required
def book_shelf_detail(request, record_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    try:
        bookshelf = get_object_or_404(BookShelfModel, id=record_id)
    except Exception as e:
        print("加入书架失败", e)
    else:
        return render(request, 'book_shelf/book_shelf_detail.html', {'bookshelf': bookshelf})
