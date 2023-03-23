from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'publisher', 'publish_time', 'price', 'book_id']
        labels = {
            'name': '书名',
            'author': '作者',
            'publisher': '出版社',
            'publish_time': '出版时间',
            'price': '价格',
            'book_id': '标识图书的唯一id'
        }
        widgets = {
            'publish_time': forms.DateInput(attrs={'type': 'date'})
        }

