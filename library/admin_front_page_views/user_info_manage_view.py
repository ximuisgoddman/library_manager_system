from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from borrow_record.borrow_record_form import BorrowRecordForm
from borrow_record.models import BorrowRecord
from users.models import MyUser


@login_required
def users_manage(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    all_users = MyUser.objects.all()
    return render(request, 'admin_front_page/users_manage.html', {'all_users': all_users})
