from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from borrow_record.borrow_record_form import BorrowRecordForm
from borrow_record.models import BorrowRecord
from users.models import MyUser


def library_front_page(request):
    return render(request, 'user_front_page/front_page.html')
