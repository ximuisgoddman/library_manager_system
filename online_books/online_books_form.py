from django import forms
from .models import OnlineBooksModel, BookShelfModel


class OnlineBooksForm(forms.ModelForm):
    file_upload = forms.FileField(required=False, label="批量上传")  # 添加文件上传字段

    class Meta:
        model = OnlineBooksModel
        fields = ['book_image', 'book_name', 'book_author', 'book_publisher', 'book_description', 'book_classification']
        labels = {
            'book_name': '书名',
            'book_author': '作者',
            'book_publisher': '出版社',
            'book_description': '图书简介',
            'book_image': '图书封面',
            'book_classification': '图书分类'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


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
