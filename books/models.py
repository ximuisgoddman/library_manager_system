from django.db import models


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
