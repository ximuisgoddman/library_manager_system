from django.db import models
from users.models import MyUser


class Book(models.Model):
    book_image = models.ImageField(upload_to='offline_book_images/')
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, db_index=True)
    publisher = models.CharField(max_length=100, db_index=True)
    publish_time = models.DateField()
    book_numbers = models.IntegerField(db_index=True)
    current_number = models.IntegerField()
    book_Introduction = models.CharField(max_length=1000)
    book_classification = models.CharField(max_length=100, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_name


class BorrowRecord(models.Model):
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    record_user_borrow_time = models.IntegerField()
    record_user_borrow_deadline = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    record_user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='borrow_record')

    def __str__(self):
        return str(self.record_user_id)
