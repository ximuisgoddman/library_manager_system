from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .book_form import BookForm
from .models import Book
from users.models import MyUser
from borrow_record.borrow_record_form import BorrowRecordForm
from django.http import QueryDict
from borrow_record.models import BorrowRecord
import datetime
from django.http import HttpResponse
import redis
import logging

# 获得logger实例
logger = logging.getLogger('myapp')

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Book


def book_front_page(request):
    publishers = Book.objects.values_list('publisher', flat=True).distinct()
    bookClasses = Book.objects.values_list('book_classification', flat=True).distinct()

    publisher = request.GET.get('publisher', '')
    book_class = request.GET.get('book_class', '')
    logger.info("filter_publisher:%s filter_book_class:%s", publisher, book_class)
    search_query = request.GET.get('search', '')
    books = Book.objects.filter(book_name__icontains=search_query)
    books = books.filter(publisher__icontains=publisher)
    books = books.filter(book_classification__icontains=book_class)

    return render(request, 'user_front_page/books_front_page.html', {
        'books': books,
        'publishers': publishers,
        'bookClasses': bookClasses})


@login_required
def book_list(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')

    publishers = Book.objects.values_list('publisher', flat=True).distinct()
    bookClasses = Book.objects.values_list('book_classification', flat=True).distinct()

    publisher = request.GET.get('publisher', '')
    book_class = request.GET.get('book_class', '')
    logger.info("filter_publisher:%s filter_book_class:%s", publisher, book_class)
    search_query = request.GET.get('search', '')
    books = Book.objects.all()
    books = books.filter(book_name__icontains=search_query)
    books = books.filter(publisher__icontains=publisher)
    books = books.filter(book_classification__icontains=book_class)

    return render(request, 'books/book_list.html', {
        'books': books,
        'publishers': publishers,
        'bookClasses': bookClasses})


@login_required
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    print("Book", book)
    return render(request, 'books/book_detail.html', {'book': book})


@login_required
def book_create(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    print("request.POST:", request.POST)
    form = BookForm(request.POST or None)
    if form.is_valid():
        book = form.save(commit=False)
        book.owner = request.user
        book.save()
        return redirect('book_list')
    return render(request, 'books/book_create.html', {'form': form})


@login_required
def book_update(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    book = Book.objects.get(id=book_id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/book_create.html', {'form': form})


@login_required
def book_delete(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_delete.html', {'book': book})


@login_required
def book_borrow(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')

    same_book_id = BorrowRecord.objects.filter(book_id=book_id, record_user_id=request.user.id).first()
    if same_book_id:
        logger.info("already borrow:%s %s" % (same_book_id.record_user_id.id, request.user.name))
        return render(request, 'borrow_record/user_borrow_record/user_borrow_record_detail.html',
                      {'record': same_book_id})
    borrow_book = Book.objects.filter(id=book_id).first()
    if borrow_book.current_number < 1:
        logger.error("borrow out")
        books = Book.objects.all()
        return render(request, 'user_front_page/books_front_page.html', {'books': books})

    # 创建redis客户端,连接到 Redis 服务器
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
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
