from django.shortcuts import render
from .online_song_form import OnlineSongForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import OnlineSongModel, MyFavoriteMusic
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import csv
import os
import json
from django.core.paginator import Paginator
from django.core.cache import cache
import base64
from online_song.tasks import sync_upload_song
from django.conf import settings

# 指定Django默认配置文件模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')


def upload_song(request):
    if request.method == 'POST':
        form = OnlineSongForm(request.POST, request.FILES)
        if form.is_valid():
            if 'file_upload' in request.FILES:
                # 处理文件上传逻辑
                file = request.FILES['file_upload']
                # 在这里异步解析文件数据并将数据写入数据库
                print("file:", file)
                user_celery = settings.USE_CELERY
                if user_celery:
                    result = sync_upload_song.delay(str(file))
                    if result.ready():
                        print("任务已完成")
                    else:
                        print("任务还在执行中")
                else:
                    sync_upload_song(str(file))
        else:
            song = form.save()
            song.save()
        return redirect('admin_online_song_list')
    else:
        form = OnlineSongForm()
    return render(request, 'online_song/upload_song.html', {'form': form})


def admin_online_song_list(request):
    songs = OnlineSongModel.objects.all()
    search_query = request.GET.get('search', '')
    songs = songs.filter(song_title__icontains=search_query)
    return render(request, 'online_song/song_list.html', {'songs': songs})


def transform_chinese(input_str):
    return base64.b64encode(input_str.encode("utf-8")).decode("utf-8")


def online_song_list(request):
    all_songs = OnlineSongModel.objects.all().order_by('id')
    all_song_authors = all_songs.values_list('song_author', flat=True)
    search_query = request.GET.get('search', '')
    song_author = request.GET.get('song_author', '')

    if search_query:
        all_songs = all_songs.filter(song_title__icontains=search_query)
    if song_author:
        all_songs = all_songs.filter(song_author__icontains=song_author)

    song_list = []
    paginator = Paginator(all_songs, per_page=20)  # 每页显示20条数据
    page_number = request.GET.get('page')
    new_cache_key = 'online_song_list_{}_{}_{}'.format(transform_chinese(song_author),
                                                       transform_chinese(search_query),
                                                       page_number)
    print("new_cache_key:", new_cache_key)
    page_obj = cache.get(new_cache_key)
    if not page_obj:
        page_obj = paginator.get_page(page_number)
        cache.set(new_cache_key, page_obj, timeout=60 * 10)
    for each_song in page_obj:
        song_list.append({"song_id": each_song.id,
                          "song_title": each_song.song_title.replace("'", " "),
                          "audio_file": each_song.audio_file.url.replace("'", " "),
                          "song_duration": each_song.song_duration.replace("'", " "),
                          "song_author": each_song.song_author.replace("'", " ")})
        each_song.song_format = each_song.audio_file.url.split(".")[-1].lower()
    if request.method == 'POST':
        return JsonResponse({"song_list": json.dumps(song_list)})
    return render(request, 'user_front_page/online_songs/song_list.html',
                  {'page_obj': page_obj,
                   'song_authors': set(all_song_authors),
                   "songs_json": json.dumps(song_list)})


@login_required
def online_song_update(request, song_id):
    song = OnlineSongModel.objects.get(id=song_id)
    form = OnlineSongForm(request.POST or None, instance=song)
    if form.is_valid():
        form.save()
        return redirect('admin_online_song_list')
    return render(request, 'online_song/upload_song.html', {'form': form})


@login_required
def online_song_delete(request, song_id):
    song = OnlineSongModel.objects.get(id=song_id)
    if request.method == 'POST':
        song.delete()
        return redirect('admin_online_song_list')
    return render(request, 'online_song/delete_online_song.html', {'song': song})


@login_required
def add_to_favorite(request):
    if request.method == "POST":
        song_id = request.POST.get("songId")
        print("song_id:", song_id)
        song = OnlineSongModel.objects.get(id=song_id)
        user = request.user
        # 创建或获取 MyFavoriteMusic 对象
        favorite_music, created = MyFavoriteMusic.objects.get_or_create(
            music_id=song.id,
            audio_file=song.audio_file,
            song_title=song.song_title,
            song_author=song.song_author,
            song_duration=song.song_duration,
            song_classification=song.song_classification,
            favorite_music_user_id=user
        )
        print("favorite_music:%s, created:%s" % (favorite_music, created))
        if created:
            return JsonResponse({"status": "success", "message": "歌曲已添加到favorite列表"})
        else:
            return JsonResponse({"status": "error", "message": "歌曲已存在于favorite列表中"})
    else:
        return JsonResponse({"status": "error", "message": "未登录或请求方法错误"})


def my_favorite_music_list(request, favorite_music_user_id):
    songs = MyFavoriteMusic.objects.filter(favorite_music_user_id=favorite_music_user_id)
    search_query = request.GET.get('search', '')
    songs = songs.filter(song_title__icontains=search_query)
    song_list = []
    for each_song in songs:
        song_list.append({"song_id": each_song.id,
                          "song_title": each_song.song_title,
                          "audio_file": each_song.audio_file.url,
                          "song_author": each_song.song_author,
                          "song_classification": each_song.song_classification})

    return render(request, 'user_front_page/online_songs/my_favorite_music.html',
                  {'songs': songs, "songs_json": json.dumps(song_list)})


@login_required
def delete_favorite_music(request, music_id):
    favorite_music = MyFavoriteMusic.objects.get(music_id=music_id)
    if request.method == 'POST':
        favorite_music.delete()
        return redirect('my_favorite_music_list', favorite_music_user_id=favorite_music.favorite_music_user_id.id)
    return render(request, 'user_front_page/online_songs/delete_favorite_music.html',
                  {'favorite_music': favorite_music})
