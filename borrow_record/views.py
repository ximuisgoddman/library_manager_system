from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .borrow_record_form import BorrowRecordForm
from .models import BorrowRecord
from users.models import MyUser


@login_required
def borrow_record(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    borrow_records = BorrowRecord.objects.all()
    return render(request, 'borrow_record/borrow_record.html', {'borrow_records': borrow_records})


@login_required
def borrow_record_detail(request, record_id):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    try:
        record = get_object_or_404(BorrowRecord, id=record_id)
    except Exception as e:
        print("图书未借阅", e)
    else:
        print("@@@", record.id, record.book_id)
        return render(request, 'borrow_record/borrow_record_detail.html', {'record': record})

