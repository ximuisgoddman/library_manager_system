from markdownx.models import MarkdownxField
from django.db import models
from users.models import MyUser


class BlogModel(models.Model):
    title = models.CharField(max_length=200)
    content = MarkdownxField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    blog_author_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='blog_author')

    def __str__(self):
        return self.title
