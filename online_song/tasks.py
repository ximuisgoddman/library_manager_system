from io import TextIOWrapper
import csv
import os
from celery import shared_task
from .models import OnlineSongModel
from library.settings import BASE_DIR


@shared_task
def sync_upload_song(file_name):
    songs_to_create = []
    file_name = os.path.join(BASE_DIR, "my_resource/music", file_name)
    print("file_name:", file_name)
    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        # 创建 CSV Reader 对象
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            song_filename = row[0].strip()
            song_full_path = os.path.join('audio', song_filename)
            song = OnlineSongModel(
                song_author=row[1],
                song_title=row[2],
                audio_file=song_full_path,
                song_duration=row[4],
                song_classification=row[3]
            )
            songs_to_create.append(song)
            # song.save()
        OnlineSongModel.objects.bulk_create(songs_to_create)
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
