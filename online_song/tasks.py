from io import TextIOWrapper
import csv
import os
from celery import shared_task
from .models import OnlineSongModel
from django.core.files.storage import default_storage


@shared_task
def sync_upload_song(file_path):
    songs_to_create = []
    with default_storage.open(file_path, 'rb') as file:
        file_wrapper = TextIOWrapper(file, encoding='utf-8')
        reader = csv.reader(file_wrapper, delimiter='|')
        for row in reader:
            print("@@@@:", row, row[6].strip())
            song = OnlineSongModel(
                song_author=row[0],
                song_title=row[1],
                audio_file=os.path.join("online_songs/audio/", row[2]),
                song_duration="{:02}:{:02}".format(int(row[3]) // 60, int(row[3]) % 60),
                song_classification=row[4],
                lrc_file=os.path.join("online_songs/lrc_file/", row[5]),
                song_image=os.path.join("online_songs/image/", row[6].strip())
            )
            songs_to_create.append(song)
            song.save()
        # OnlineSongModel.objects.bulk_create(songs_to_create)
# @shared_task
# def generate_static_page(page_id, page_title, page_body):
#     # 模拟耗时任务，比如写入文件或发送邮件等操作。
#     time.sleep(5)
#
#     # 获取传递的参数
#     page = {'title': page_title, 'body': page_body}
#     context = {'page': page, }
#
#     # 渲染模板，生成字符串
#     content = render_to_string('staticpage/template.html', context)
#
#     # 定义生成静态文件所属目录，位于media文件夹下名为html的子文件夹里。如目录不存在，则创建。
#     directory = os.path.join(settings.MEDIA_ROOT, "html")
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#
#     # 拼接目标写入文件地址
#     static_html_path = os.path.join(directory, 'page_{}.html'.format(page_id))
#
#     # 将渲染过的字符串写入目标文件
#     with open(static_html_path, 'w', encoding="utf-8") as f:
#         f.write(content)
