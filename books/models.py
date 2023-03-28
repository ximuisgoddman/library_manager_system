from django.db import models
from users.models import MyUser


class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    publish_time = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.name
