from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_name', 'author', 'publisher', 'publish_time', 'book_numbers', 'book_id']
        labels = {
            'book_name': '书名',
            'author': '作者',
            'publisher': '出版社',
            'publish_time': '出版时间',
            'book_numbers': '数量',
            'book_id': '标识图书的唯一id'
        }
        widgets = {
            'publish_time': forms.DateInput(attrs={'type': 'date'})
        }

