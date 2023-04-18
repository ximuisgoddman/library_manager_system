from django.db import models
from users.models import MyUser


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
