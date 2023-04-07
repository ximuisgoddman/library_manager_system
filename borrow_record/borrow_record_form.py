from django import forms
from .models import BorrowRecord


class BorrowRecordForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['record_user_borrow_time', 'record_user_borrow_deadline', 'book_name', 'book_author', 'publisher',
                  'book_id', 'record_user_id']
        labels = {
            'book_name': '书籍名称',
            'book_author': '书籍作者',
            'publisher': '出版社',
            'record_user_borrow_time': '借阅时间',
            'record_user_borrow_deadline': '归还截至日期',
            'book_id': '图书唯一标识',
            'record_user_id': '图书借阅者id',
        }
