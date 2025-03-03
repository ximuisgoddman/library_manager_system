from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .book_form import BookForm, BorrowRecordForm
from .models import Book, BorrowRecord
from django.http import QueryDict
import datetime
from django.http import HttpResponse
import redis
import logging
import os
from library.utils import handle_uploaded_file
from .tasks import sync_upload_book

# 获得logger实例
logger = logging.getLogger('myapp')
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings

# 指定Django默认配置文件模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')


def book_front_page(request):
    publishers = Book.objects.values_list('publisher', flat=True).distinct()
    bookClasses = Book.objects.values_list('book_classification', flat=True).distinct()

    publisher = request.GET.get('publisher', '')
    book_class = request.GET.get('book_class', '')
    logger.info("filter_publisher:%s filter_book_class:%s", publisher, book_class)

    search_query = request.GET.get('search', '')
    cache_key = 'book_front_page_{}'.format(search_query)
    books = cache.get(cache_key)
    if not books:
        books = Book.objects.all()
        cache.set(cache_key, books, timeout=60 * 5)  # 设置缓存时间为 5 分钟
    # 根据作者或者书名搜索
    books = books.filter(Q(book_name__icontains=search_query) | Q(author__icontains=search_query))
    # 过滤出版社和图书类别
    books = books.filter(publisher__icontains=publisher)
    books = books.filter(book_classification__icontains=book_class).order_by('id')

    paginator = Paginator(books, per_page=10)  # 每页显示10条数据

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_front_page/books_front_page.html', {
        'page_obj': page_obj,
        'publishers': publishers,
        'bookClasses': bookClasses})


@login_required
def admin_book_list(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')

    publishers = Book.objects.values_list('publisher', flat=True).distinct()
    bookClasses = Book.objects.values_list('book_classification', flat=True).distinct()

    publisher = request.GET.get('publisher', '')
    book_class = request.GET.get('book_class', '')
    logger.info("filter_publisher:%s filter_book_class:%s", publisher, book_class)
    search_query = request.GET.get('search', '')
    cache_key = 'book_list_{}'.format(search_query)
    books = cache.get(cache_key)
    if not books:
        books = Book.objects.all()
        cache.set(cache_key, books, timeout=60 * 5)

    books = books.filter(book_name__icontains=search_query)
    books = books.filter(publisher__icontains=publisher)
    books = books.filter(book_classification__icontains=book_class)

    return render(request, 'books/admin_book_list.html', {
        'books': books,
        'publishers': publishers,
        'bookClasses': bookClasses})


def user_book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'user_front_page/offline_book_detail.html', {'book': book})


@login_required
def book_detail(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    book = Book.objects.get(id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})


@login_required
def book_create(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            if 'file_upload' in request.FILES:
                # 处理文件上传逻辑
                file = request.FILES['file_upload']
                # 在这里解析文件数据并将数据写入数据库
                file_path = handle_uploaded_file(file)
                user_celery = settings.USE_CELERY
                print("file:", file, user_celery, bool(user_celery))
                if user_celery:
                    result = sync_upload_book.delay(file_path)
                    if result.ready():
                        print("任务已完成")
                    else:
                        print("任务还在执行中")
                else:
                    sync_upload_book(file_path)

                return redirect('admin_book_list')
            else:
                book = form.save(commit=False)
                # book.owner = request.user
                book.save()
                return redirect('admin_book_list')
    else:
        form = BookForm()

    return render(request, 'books/book_create.html', {'form': form})


@login_required
def book_update(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    book = Book.objects.get(id=book_id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('admin_book_list')
    return render(request, 'books/book_create.html', {'form': form})


@login_required
def book_delete(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('admin_book_list')
    return render(request, 'books/book_delete.html', {'book': book})


@login_required
def book_borrow(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')

    same_book_id = BorrowRecord.objects.filter(book_id=book_id, record_user_id=request.user.id).first()
    if same_book_id:
        logger.info("already borrow:%s %s" % (same_book_id.record_user_id.id, request.user.username))
        return render(request, 'borrow_record/user_borrow_record/user_borrow_record_detail.html',
                      {'record': same_book_id})
    borrow_book = Book.objects.filter(id=book_id).first()
    if borrow_book.current_number < 1:
        logger.error("borrow out")
        books = Book.objects.all()
        return render(request, 'user_front_page/books_front_page.html', {'books': books})

    # 创建redis客户端,连接到 Redis 服务器
    redis_client = redis.StrictRedis(host='redis' if settings.IF_RUN_ON_DOCKER else 'localhost', port=6379, db=0)
    # 使用 setnx() 方法尝试获取锁。如果获取失败，则说明有其他请求已经获取了锁，这里直接返回 HttpResponse('borrowing in progress')
    lock_key = f"borrow_lock_{book_id}"
    is_locked = redis_client.setnx(lock_key, 1)
    logger.info("is_locked:%s", is_locked)
    if not is_locked:
        # 获取锁失败
        return HttpResponse('borrowing in progress')

    try:
        # 如果获取锁成功，则使用 Redis 事务来执行关键代码。
        # 在事务开始之前，首先使用 watch() 方法监视锁的状态，如果锁已经被其他请求释放，则事务会回滚并重试。
        with redis_client.pipeline() as pipe:
            while True:
                try:
                    # 开启事务
                    pipe.watch(lock_key)
                    if not pipe.exists(lock_key):  # 检查锁是否仍然存在，如果不存在，则重试
                        continue
                    # 尝试获取锁
                    pipe.multi()  # 使用 multi() 方法开启事务。然后设置锁的过期时间为 1 秒，并执行事务。
                    pipe.expire(lock_key, 1)
                    pipe.execute()
                    # 在事务执行成功后，使用 lock() 方法创建一个 Redis 锁，设置超时时间为 1 秒，并尝试获取锁。
                    # 如果获取成功，则说明当前请求获得了锁，可以执行关键代码。如果获取失败，则说明锁已经被其他请求获取，当前请求需要重试
                    redis_lock = redis_client.lock(lock_key, timeout=1)
                    if redis_lock.acquire():
                        # 加锁成功，执行代码

                        borrow_book = Book.objects.filter(id=book_id).first()
                        print("borrow_book", borrow_book)
                        form_datas = {
                            "book_id": borrow_book.id,
                            "book_name": borrow_book.book_name,
                            "book_author": borrow_book.author,
                            "publisher": borrow_book.publisher,
                            "record_user_borrow_time": 10,
                            "record_user_borrow_deadline": datetime.datetime.now(),
                            "record_user_id": request.user.id
                        }
                        form_data = QueryDict('', mutable=True)
                        form_data.update(form_datas)
                        form = BorrowRecordForm(form_data)
                        print("Error", form.errors, form_data)
                        if form.is_valid():
                            form.save()
                        # 借书成功，并且书籍数量-1
                        borrow_book.current_number = borrow_book.current_number - 1
                        borrow_book.save()

                        borrow_records = BorrowRecord.objects.filter(record_user_id=request.user.id)
                        return render(request, 'borrow_record/user_borrow_record/user_borrow_record_list.html',
                                      {'borrow_records': borrow_records})
                    break
                except redis.WatchError:
                    continue
    except Exception as e:
        print(e)
    finally:
        # 释放锁
        redis_client.delete(lock_key)


@login_required
def user_borrow_record(request, record_user_id):
    print("qqrequest.user:", request.user, record_user_id)
    if not request.session.get("is_login", None):
        return redirect('/login/')
    borrow_records = BorrowRecord.objects.filter(record_user_id=record_user_id)
    return render(request, 'borrow_record/user_borrow_record/user_borrow_record_list.html',
                  {'borrow_records': borrow_records})


@login_required
def user_borrow_record_detail(request, record_id):
    print("request.user:", request.user, record_id)
    if not request.session.get("is_login", None):
        return redirect('/login/')
    try:
        record = get_object_or_404(BorrowRecord, id=record_id)
    except Exception as e:
        print("图书未借阅", e)
    else:
        print("@@@", record.id, record.book_id)
        return render(request, 'borrow_record/user_borrow_record/user_borrow_record_detail.html', {'record': record})


@login_required
def admin_borrow_record(request, record_user_id):
    print("qqrequest.user:", request.user, record_user_id)
    if not request.session.get("is_login", None):
        return redirect('/login/')
    borrow_records = BorrowRecord.objects.filter(record_user_id=record_user_id)
    return render(request, 'borrow_record/admin_borrow_record/admin_borrow_record_list.html',
                  {'borrow_records': borrow_records})


@login_required
def admin_borrow_record_detail(request, record_id):
    print("request.user:", request.user, record_id)
    if not request.session.get("is_login", None):
        return redirect('/login/')
    try:
        record = get_object_or_404(BorrowRecord, id=record_id)
    except Exception as e:
        print("图书未借阅", e)
    else:
        print("@@@", record.id, record.book_id)
        return render(request, 'borrow_record/admin_borrow_record/admin_borrow_record_detail.html', {'record': record})
