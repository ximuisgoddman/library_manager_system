from django.db import models
from users.models import MyUser


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
