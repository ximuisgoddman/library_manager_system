from .online_books_form import OnlineBooksForm, BookShelfForm
from .models import OnlineBooksModel, BookShelfModel
from users.models import MyUser
from django.core.cache import cache
from io import TextIOWrapper
import csv
import requests
import shutil
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import os
import zipfile
from bs4 import BeautifulSoup
from django.db.models import Q
from django.core.paginator import Paginator


def user_online_book_list(request):
    book_publishers = OnlineBooksModel.objects.values_list('book_publisher', flat=True).distinct()
    bookClasses = OnlineBooksModel.objects.values_list('book_classification', flat=True).distinct()

    book_publisher = request.GET.get('book_publisher', '')
    book_class = request.GET.get('book_class', '')
    search_query = request.GET.get('search', '')
    cache_key = 'user_online_book_list_{}'.format(search_query)
    online_books = cache.get(cache_key)
    if online_books is None:
        online_books = OnlineBooksModel.objects.all()
        cache.set(cache_key, online_books, timeout=60 * 5)  # 设置缓存时间为 5 分钟
    # 根据作者或者书名搜索
    online_books = online_books.filter(Q(book_name__icontains=search_query) | Q(book_author__icontains=search_query))
    # 过滤出版社和图书类别
    online_books = online_books.filter(book_publisher__icontains=book_publisher)
    online_books = online_books.filter(book_classification__icontains=book_class).order_by('id')
    print(book_publisher, len(online_books))
    paginator = Paginator(online_books, per_page=10)  # 每页显示10条数据

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user_front_page/online_books_front_page.html',
                  {'page_obj': page_obj,
                   'publishers': book_publishers,
                   'bookClasses': bookClasses})


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
    epub_file_path = os.path.join("media/", book.book_save_path)

    # 创建一个目录来保存 EPUB 文件中的资源
    resource_dir = os.path.join("media/", str(book_id))
    os.makedirs(resource_dir, exist_ok=True)

    # 读取 EPUB 文件
    with zipfile.ZipFile(epub_file_path, 'r') as epub_zip:
        # 提取章节内容并转换为 HTML 格式
        chapters = []
        for filename in epub_zip.namelist():
            if filename.endswith('.html'):
                with epub_zip.open(filename, 'r') as f:
                    # 解码 HTML 编码的字符串
                    decoded_content = f.read().decode('utf-8')
                    # 使用 BeautifulSoup 解析 HTML 内容
                    soup = BeautifulSoup(decoded_content, 'html.parser')

                    # 处理图片和其他资源
                    for img_tag in soup.find_all("img", src=True):
                        src = img_tag["src"]
                        handle_resource(src, resource_dir, epub_zip)

                    for link_tag in soup.find_all("link", href=True):
                        href = link_tag["href"]
                        handle_resource(href, resource_dir, epub_zip)

                    for script_tag in soup.find_all("script", src=True):
                        src = script_tag["src"]
                        handle_resource(src, resource_dir, epub_zip)

                    # 获取章节标题和内容
                    title = os.path.basename(filename)
                    content = str(soup)
                    chapters.append({'title': title, 'content': content})

    return render(request, "user_front_page/read_online_book.html", {'chapters': chapters,
                                                                     'chapter_count': len(chapters)})


def handle_resource(src, resource_dir, epub_zip):
    if src.startswith("http"):
        # 如果资源是一个 URL，则下载它
        response = requests.get(src)
        filename = os.path.basename(src)
        dest_path = os.path.join(resource_dir, filename)
        with open(dest_path, "wb") as f:
            f.write(response.content)
    else:
        # 如果资源是一个文件路径，则拷贝它
        try:
            with epub_zip.open(src, 'r') as src_file:
                filename = os.path.basename(src)
                dest_path = os.path.join(resource_dir, filename)
                with open(dest_path, "wb") as dest_file:
                    print("src_file:", src_file)
                    shutil.copyfileobj(src_file, dest_file)
        except KeyError:
            print(f"File {src} not found in EPUB archive.")


@login_required
def add_book_shelf(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')

    bookshelf = BookShelfModel.objects.filter(book_id=book_id, book_shelf_user_id=request.user.id)
    if bookshelf:
        print("already add to shelf", bookshelf)
        return render(request, 'book_shelf/user_book_shelf/user_book_shelf_list.html',
                      {'bookshelfs': BookShelfModel.objects.filter(book_shelf_user_id=request.user.id)})

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
    bookshelfs = BookShelfModel.objects.filter(book_shelf_user_id=request.user.id)
    return render(request, 'book_shelf/user_book_shelf/user_book_shelf_list.html', {'bookshelfs': bookshelfs})


@login_required
def user_book_shelf_list(request, book_shelf_user_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    bookshelfs = BookShelfModel.objects.filter(book_shelf_user_id=book_shelf_user_id)
    return render(request, 'book_shelf/user_book_shelf/user_book_shelf_list.html', {'bookshelfs': bookshelfs})


@login_required
def delete_book_shelf(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    try:
        bookshelf = get_object_or_404(BookShelfModel, book_id=book_id)
        if request.method == 'POST':
            bookshelf.delete()
            return redirect('user_book_shelf_list', book_shelf_user_id=bookshelf.book_shelf_user_id.id)
    except Exception as e:
        print("删除书架失败", e)
    else:
        return render(request, 'book_shelf/user_book_shelf/delete_book_shelf.html', {'bookshelf': bookshelf})


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
