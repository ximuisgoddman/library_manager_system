# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

# 指定Django默认配置文件模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

# 为我们的项目myproject创建一个Celery实例, 并设置redis做broker，否则启动失败
app = Celery('library', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

# 这里指定从django的settings.py里读取celery配置
app.config_from_object('django.conf:settings')

# 自动从所有已注册的django app中加载任务
app.autodiscover_tasks(['article.tasks.update_article_likes', 'online_song.tasks.test_celery'])
app.conf.beat_schedule = {
    'update_likes_every_hour': {
        'task': 'article.tasks.update_article_likes',
        'schedule': timedelta(seconds=10),
    },
}


# 用于测试的异步任务
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
