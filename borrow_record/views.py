from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .borrow_record_form import BorrowRecordForm
from .models import BorrowRecord
from users.models import MyUser


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
