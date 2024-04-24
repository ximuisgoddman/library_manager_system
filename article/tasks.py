# encoding：utf-8
from celery import shared_task
from .models import ArticlePost
from library.settings import BASE_DIR
from django.core.cache import cache


@shared_task
def update_article_likes_collect():
    all_article_ids = ArticlePost.objects.values('id')
    for each_id in all_article_ids:
        _likes = cache.get("article_%s_likes" % each_id['id'])
        if _likes:
            ArticlePost.objects.filter(id=each_id['id']).update(likes=_likes)
        _collect = cache.get("article_%s_collect" % each_id['id'])
        if _collect:
            ArticlePost.objects.filter(id=each_id['id']).update(collects=_collect)
