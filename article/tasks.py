# encoding：utf-8
from celery import shared_task
from .models import ArticlePost
from library.settings import BASE_DIR
from django.core.cache import cache


@shared_task
def update_article_likes():
    all_article_ids = ArticlePost.objects.values('id')
    for each_id in all_article_ids:
        _likes = cache.get("library::1:article_%s_likes" % each_id)
        print("KK:", _likes)
        if _likes:
            ArticlePost.objects.get(id=each_id).update(likes=_likes)
