from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .book_form import BookForm
from .models import Book
from users.models import MyUser
from borrow_record.borrow_record_form import BorrowRecordForm
from django.http import QueryDict
from borrow_record.models import BorrowRecord
import datetime


def book_front_page(request):
    search_query = request.GET.get('search', '')
    books = Book.objects.filter(book_name__icontains=search_query)
    return render(request, 'user_front_page/books_front_page.html', {'books': books})


@login_required
def book_list(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    search_query = request.GET.get('search', '')
    books = Book.objects.filter(book_name__icontains=search_query)
    # books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


@login_required
def book_detail(request, book_id):
    book = Book.objects.get(book_id=book_id)
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
    book = Book.objects.get(book_id=book_id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/book_create.html', {'form': form})


@login_required
def book_delete(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    book = Book.objects.get(book_id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_delete.html', {'book': book})


@login_required
def book_borrow(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')

    same_book_id = BorrowRecord.objects.filter(book_id=book_id).first()
    if same_book_id:
        print("already borrow", same_book_id.record_user_id.id)
        return render(request, 'borrow_record/borrow_record_detail.html', {'record': same_book_id})
    print("Lee",Book.objects.filter(book_id=book_id))
    if Book.objects.filter(book_id=book_id).first().book_numbers < 1:
        print("borrow out", )
        books = Book.objects.all()
        return render(request, 'user_front_page/books_front_page.html', {'books': books})
    borrow_book = Book.objects.filter(book_id=book_id).first()
    print("borrow_book", borrow_book)
    form_datas = {
        "book_name": borrow_book.book_name,
        "book_author": borrow_book.author,
        "publisher": borrow_book.publisher,
        "record_user_borrow_time": 10,
        "record_user_borrow_deadline": datetime.datetime.now(),
        "book_id": int(borrow_book.book_id),
        "record_user_id": request.user.id
    }
    form_data = QueryDict('', mutable=True)
    form_data.update(form_datas)
    form = BorrowRecordForm(form_data)
    print("Error", form.errors, form_data)
    if form.is_valid():
        form.save()
    borrow_book.book_numbers=borrow_book.book_numbers-1
    borrow_book.save()

    # borrow_records = BorrowRecord.objects.get(book_id=int(borrow_book.book_id))
    borrow_records = BorrowRecord.objects.filter(record_user_id=request.user.id)
    print("Len", len(borrow_records))
    return render(request, 'borrow_record/borrow_record.html', {'borrow_records': borrow_records})
