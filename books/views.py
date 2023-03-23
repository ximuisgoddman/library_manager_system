from django.shortcuts import render, redirect
from .models import Book
from .book_form import BookForm


def book_list(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


def book_detail(request, book_id):
    book = Book.objects.get(book_id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})


def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/book_create.html', {'form': form})


def book_update(request, book_id):
    book = Book.objects.get(book_id=book_id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'books/book_create.html', {'form': form})


def book_delete(request, book_id):
    book = Book.objects.get(book_id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/book_delete.html', {'book': book})
