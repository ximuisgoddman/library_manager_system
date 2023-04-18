from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .online_books_form import OnlineBooksForm
from .models import OnlineBooksModel
from users.models import MyUser
from django.http import QueryDict
from bookshelf.models import BookShelfModel
from bookshelf.book_shelf_form import BookShelfForm


# Create your views here.
@login_required
def online_book_list(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    # books = Book.objects.filter(owner=request.user)
    books = OnlineBooksModel.objects.all()
    return render(request, 'online_books/online_books_front_page.html', {'books': books})


@login_required
def online_book_create(request):
    print("request.POST:", request.POST)
    form = OnlineBooksForm(request.POST, request.FILES)
    if form.is_valid():
        book = form.save(commit=False)
        # book.owner = request.user
        book.save()
        return redirect('online_book_list')
    return render(request, 'online_books/online_book_create.html', {'form': form})


@login_required
def online_book_detail(request, book_id):
    print("book_id:", book_id)
    book = OnlineBooksModel.objects.get(id=book_id)
    print("Book", book)
    return render(request, 'online_books/online_book_detail.html', {'book': book})


@login_required
def online_book_update(request, book_id):
    book = OnlineBooksModel.objects.get(book_id=book_id)
    form = OnlineBooksForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'online_books/online_book_create.html', {'form': form})


@login_required
def online_book_delete(request, book_id):
    book = get_object_or_404(request.user.books, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'online_books/online_book_delete.html', {'book': book})


@login_required
def add_book_shelf(request, book_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')

    bookshelf = BookShelfModel.objects.filter(id=book_id).first()
    if bookshelf:
        print("already add to shelf")
        return render(request, 'book_shelf/book_shelf_detail.html', {'bookshelf': bookshelf})

    online_book = OnlineBooksModel.objects.filter(id=book_id).first()
    print("online_book", online_book,type(online_book.book_image))
    form_datas = {
        "book_name": online_book.book_name,
        "book_author": online_book.book_author,
        "book_publisher": online_book.book_publisher,
        "book_image": online_book.book_image,
        "book_id": online_book.id,
        'book_shelf_user_id': request.user.id
    }
    form_data = QueryDict('', mutable=True)
    form_data.update(form_datas)
    form = BookShelfForm(form_data, request.FILES)
    print("Error", form.errors, "form_data:%s" % form_data)
    if form.is_valid():
        from django.core.files import File
        from io import BytesIO
        bookshelf = form.save(commit=False)
        # 将 ImageFieldFile 对象转换为 File 对象
        if bookshelf.book_image:
            in_memory_file = BytesIO()
            bookshelf.book_image.save(in_memory_file, bookshelf.book_image.format)
            bookshelf.book_image = File(in_memory_file, name=bookshelf.book_image.name)
        bookshelf.save()
    bookshelfs = BookShelfModel.objects.all()
    print("Len", len(bookshelfs), request.FILES)
    for x in bookshelfs:
        print("@@", x.id, x.book_name,x.book_image)
    return render(request, 'book_shelf/book_shelf_list.html', {'bookshelfs': bookshelfs})
