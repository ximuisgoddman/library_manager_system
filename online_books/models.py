from django.db import models
from users.models import MyUser


# Create your models here.
class OnlineBooksModel(models.Model):
    book_image = models.ImageField(upload_to='online_book_images/')
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100, db_index=True)
    book_publisher = models.CharField(max_length=100, db_index=True)
    book_classification = models.CharField(max_length=100, db_index=True)
    book_save_path = models.CharField(max_length=100)
    book_description = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_name


class BookShelfModel(models.Model):
    book_image = models.ImageField(blank=False, null=False)
    book_id = models.IntegerField()
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    book_publisher = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    book_shelf_user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='book_shelf_user_id')

    def __str__(self):
        return str(self.book_shelf_user_id)
