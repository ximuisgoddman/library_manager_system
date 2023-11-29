from django.db import models
from users.models import MyUser
from article.models import ArticlePost


class MyFavoriteArtile(models.Model):
    favorite_article_id = models.ForeignKey(ArticlePost,
                                            on_delete=models.CASCADE,
                                            related_name='favorite_article_id')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    favorite_article_user_id = models.ForeignKey(MyUser,
                                                 on_delete=models.CASCADE,
                                                 related_name='favorite_article_user_id')

    def __str__(self):
        return str(self.favorite_article_user_id)
