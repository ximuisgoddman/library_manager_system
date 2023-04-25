from django.db import models


# Create your models here.
class OnlineBooksModel(models.Model):
    book_image = models.ImageField(upload_to='online_book_images/')
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    book_publisher = models.CharField(max_length=100)
    book_classification = models.CharField(max_length=100)
    book_save_path = models.CharField(max_length=100)
    book_description = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_name
