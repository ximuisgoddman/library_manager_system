from django import forms
from .models import OnlineBooksModel


class OnlineBooksForm(forms.ModelForm):
    file_upload = forms.FileField(required=False)  # 添加文件上传字段
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
