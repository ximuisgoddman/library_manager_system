from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .borrow_record_form import BorrowRecordForm
from .models import BorrowRecord
from users.models import MyUser


# @login_required
def borrow_record_view(request, record_id):
    # if not request.session.get("is_login", None):
    #     return redirect('/login/')
    borrow_records = BorrowRecord.objects.filter(record_id=record_id)
    return render(request, 'borrow_record/borrow_record.html', {'borrow_records': borrow_records})

#
# @login_required
# def book_detail(request, book_id):
#     book = get_object_or_404(request.user.books, pk=book_id)
#     return render(request, 'books/book_detail.html', {'book': book})
#
#
# @login_required
# def book_create(request):
#     form = BookForm(request.POST or None)
#     if form.is_valid():
#         book = form.save(commit=False)
#         print("create,", request.__dict__)
#         book.owner = request.user
#         book.save()
#         return redirect('book_list')
#     return render(request, 'books/book_create.html', {'form': form})
#
#
# @login_required
# def book_update(request, book_id):
#     book = get_object_or_404(request.user.books, pk=book_id)
#     form = BookForm(request.POST or None, instance=book)
#     if form.is_valid():
#         form.save()
#         return redirect('book_list')
#     return render(request, 'books/book_create.html', {'form': form})
#
#
# @login_required
# def book_delete(request, book_id):
#     book = get_object_or_404(request.user.books, pk=book_id)
#     if request.method == 'POST':
#         book.delete()
#         return redirect('book_list')
#     return render(request, 'books/book_delete.html', {'book': book})
