from django.db import models


class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    publish_time = models.DateField()
    book_numbers = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_name
