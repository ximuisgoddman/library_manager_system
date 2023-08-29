from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .online_books_form import OnlineBooksForm
from .models import OnlineBooksModel
from users.models import MyUser
from django.http import QueryDict
from bookshelf.models import BookShelfModel
from bookshelf.book_shelf_form import BookShelfForm
from django.core.cache import cache
import os
from io import TextIOWrapper
import csv
from django.http import HttpResponse
import ebooklib
from ebooklib import epub
from io import BytesIO


def user_online_book_list(request):
    search_query = request.GET.get('search', '')
    cache_key = 'book_list_{}'.format(search_query)
    books = cache.get(cache_key)
    if books is None:
        books = OnlineBooksModel.objects.filter(book_name__icontains=search_query)
        cache.set(cache_key, books, timeout=60 * 5)  # 设置缓存时间为 5 分钟
    return render(request, 'user_front_page/online_books_front_page.html', {'books': books})


# Create your views here.
@login_required
def admin_online_book_list(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    search_query = request.GET.get('search', '')
    books = OnlineBooksModel.objects.filter(book_name__icontains=search_query)
    return render(request, 'online_books/online_books_list.html', {'books': books})


@login_required
def online_book_create(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    if request.method == 'POST':
        form = OnlineBooksForm(request.POST, request.FILES)
        print("request:", request.FILES)
        if form.is_valid():
            if 'file_upload' in request.FILES:
                # 处理文件上传逻辑
                file = request.FILES['file_upload']
                # 在这里解析文件数据并将数据写入数据库
                print("file:", file)
                file_wrapper = TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(file_wrapper)
                for row in reader:
                    # 解析CSV文件内容并创建书籍对象
                    # book_image_path = row[7]
                    book_image_filename = row[0].strip() + '.jpg'
                    book_image_full_path = os.path.join('offline_book_images/', book_image_filename)
                    book = OnlineBooksModel(
                        book_name=row[0],
                        book_author=row[1],
                        book_publisher=row[2],
                        book_save_path=os.path.join('online_books/', row[3]),
                        book_classification=row[4],
                        book_image=book_image_full_path  # 设置书籍图片路径
                    )
                    print("book_image_full_path", book_image_full_path)
                    book.owner = request.user
                    book.save()

                return redirect('admin_online_book_list')
            else:
                book = form.save(commit=False)
                book.owner = request.user
                book.save()
                return redirect('admin_online_book_list')
    else:
        form = OnlineBooksForm()

    return render(request, 'online_books/online_book_create.html', {'form': form})


@login_required
def online_book_detail(request, book_id):
    print("book_id:", book_id)
    book = OnlineBooksModel.objects.get(id=book_id)
    print("Book", book)
    return render(request, 'online_books/online_book_detail.html', {'book': book})


@login_required
def online_book_update(request, book_id):
    book = OnlineBooksModel.objects.get(id=book_id)
    form = OnlineBooksForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('admin_online_book_list')
    return render(request, 'online_books/online_book_create.html', {'form': form})


@login_required
def online_book_delete(request, book_id):
    book = OnlineBooksModel.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('admin_online_book_list')
    return render(request, 'online_books/online_book_delete.html', {'book': book})


@login_required
def read_online_book(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')

    book = get_object_or_404(OnlineBooksModel, pk=book_id)
    # book_path = book.book_save_path
    # print("book_path:", book_path)
    # book_path = os.path.join("media/",book.book_save_path)  # 获取保存电子书的路径
    # book_path = book.book_save_path
    return render(request, "user_front_page/online_songs/read_online_book.html", {"book": book})


@login_required
def add_book_shelf(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')

    bookshelf = BookShelfModel.objects.filter(id=book_id, book_shelf_user_id=request.user.id).first()
    if bookshelf:
        print("already add to shelf")
        return render(request, 'book_shelf/user_book_shelf/user_book_shelf_detail.html', {'bookshelf': bookshelf})

    online_book = OnlineBooksModel.objects.filter(id=book_id).first()
    print("online_book", online_book, type(online_book.book_image))
    if online_book:
        bookshelf = BookShelfModel(
            book_id=online_book.id,
            book_name=online_book.book_name,
            book_author=online_book.book_author,
            book_publisher=online_book.book_publisher,
            book_image=online_book.book_image,
            book_shelf_user_id=request.user
        )
        bookshelf.save()

    bookshelfs = BookShelfModel.objects.all()
    print("Len", len(bookshelfs), request.FILES)
    for x in bookshelfs:
        print("@@", x.id, x.book_name, x.book_image)
    return render(request, 'book_shelf/user_book_shelf/user_book_shelf_list.html', {'bookshelfs': bookshelfs})
