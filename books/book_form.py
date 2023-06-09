from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    BOOK_CLASS_CHOICES = [
        ('AA', 'AA'),
        ('BB', 'BB'),
        ('CC', 'CC'),
    ]
    book_classification = forms.ChoiceField(choices=BOOK_CLASS_CHOICES)
    file_upload = forms.FileField(required=False)  # 添加文件上传字段

    class Meta:
        model = Book
        fields = ['book_image', 'book_name', 'author', 'publisher', 'publish_time', 'book_numbers', 'current_number',
                  'book_classification']
        labels = {
            'book_image': '图书封面',
            'book_name': '书名:',
            'author': '作者:',
            'publisher': '出版社:',
            'publish_time': '出版时间:',
            'book_numbers': '数量:',
            'current_number': '当前数量:',
            'book_classification': '图书分类:'
        }
        widgets = {
            'publish_time': forms.DateInput(attrs={'type': 'date'})
        }
