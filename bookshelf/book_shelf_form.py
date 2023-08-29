from django import forms
from .models import BookShelfModel


class BookShelfForm(forms.ModelForm):
    class Meta:
        model = BookShelfModel
        fields = ['book_id', 'book_name', 'book_image', 'book_author', 'book_publisher', 'book_shelf_user_id']
        labels = {
            'book_name': '书籍名称',
            'book_author': '书籍作者',
            'book_publisher': '出版社',
            'book_id': '图书唯一标识',
            'book_image': '图书封面',
            'book_shelf_user_id': '书架拥有者id'
        }
