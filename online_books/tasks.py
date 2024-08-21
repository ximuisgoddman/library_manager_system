import os
from django.core.files.storage import default_storage
from .models import OnlineBooksModel
from celery import shared_task
from io import TextIOWrapper
import csv


@shared_task
def sync_upload_online_book(file_path):
    # 打开保存的文件
    with default_storage.open(file_path, 'rb') as file:
        file_wrapper = TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(file_wrapper)
        for row in reader:
            # 解析CSV文件内容并创建书籍对象
            book_image_filename = row[0].strip() + '.jpg'
            book_image_full_path = os.path.join('offline_book_images/', book_image_filename)
            book = OnlineBooksModel(
                book_name=row[0],
                book_author=row[1],
                book_publisher=row[2],
                book_save_path=os.path.join('online_books/', row[3]),
                book_classification=row[4],
                book_image=book_image_full_path  # 设置书籍图片路径
            )
            book.save()
