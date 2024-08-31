from django.shortcuts import render
from .online_song_form import OnlineSongForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import OnlineSongModel, MyFavoriteMusic
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.templatetags.static import static
import os
import json
from django.core.paginator import Paginator
from django.core.cache import cache
import base64
from online_song.tasks import sync_upload_song
from django.conf import settings
from library.utils import handle_uploaded_file
from urllib.parse import unquote

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
                file_path = handle_uploaded_file(file)
                print("file:", file_path)
                user_celery = settings.USE_CELERY
                if user_celery:
                    result = sync_upload_song.delay(file_path)
                    if result.ready():
                        print("任务已完成")
                    else:
                        print("任务还在执行中")
                else:
                    sync_upload_song(file_path)
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
    print()
    page_obj = cache.get(new_cache_key)
    if not page_obj:
        page_obj = paginator.get_page(page_number)
        cache.set(new_cache_key, page_obj, timeout=60 * 10)
    for each_song in page_obj:
        if not each_song.song_image or not os.path.exists(each_song.song_image.path):
            each_song.song_image = 'avatar/default.jpg'
        song_list.append({"song_id": each_song.id,
                          "song_title": each_song.song_title,
                          "audio_file": each_song.audio_file.url,
                          "song_duration": each_song.song_duration,
                          "song_author": each_song.song_author})
    # if request.method == 'POST':
    #     return JsonResponse({"song_list": json.dumps(song_list)})
    return render(request, 'user_front_page/online_songs/song_list.html',
                  {'page_obj': page_obj,
                   'selected_song_author': song_author,
                   'song_authors': set(all_song_authors),
                   "songs_json": json.dumps(song_list),
                   "current_song_json": json.dumps(song_list[0]) if len(song_list) > 0 else {}})


def play_online_song(request, song_id):
    # 获取歌曲对象
    current_song = get_object_or_404(OnlineSongModel, pk=song_id)
    if not current_song.song_image or not os.path.exists(current_song.song_image.path):
        current_song.song_image = 'avatar/default.jpg'
    search_query = request.GET.get('search', '')
    song_author = request.GET.get('song_author', '')
    song_classification = request.GET.get('song_classification', '')
    page_number = request.GET.get('page', 1)
    filtered_songs = OnlineSongModel.objects.all().order_by('id')
    song_list = []
    if search_query:
        filtered_songs = filtered_songs.filter(song_title__icontains=search_query)
    if song_author:
        filtered_songs = filtered_songs.filter(song_author=song_author)
    if song_classification:
        filtered_songs = filtered_songs.filter(song_classification=song_classification)
    page_obj = Paginator(filtered_songs, per_page=20).get_page(page_number)
    for each_song in page_obj:
        if not each_song.song_image or not os.path.exists(each_song.song_image.path):
            each_song.song_image = 'avatar/default.jpg'

        song_list.append({"song_id": each_song.id,
                          "song_title": each_song.song_title,
                          "audio_file": each_song.audio_file.url,
                          "song_duration": each_song.song_duration,
                          "song_author": each_song.song_author})

    # 歌词文件路径
    lrc_file_path = os.path.join(settings.BASE_DIR, "media", str(current_song.lrc_file))
    lyrics = "暂无歌词"
    # 读取 LRC 歌词文件内容
    try:
        with open(lrc_file_path, 'r', encoding='utf-8') as file:
            lyrics = file.read()
    except FileNotFoundError:
        print(f"LRC file not found: {lrc_file_path}")  # 调试信息

    context = {
        'current_song': current_song,
        'lyrics': lyrics,
        'artist': current_song.song_author,  # 歌手
        'album': current_song.song_classification,
        "songs_json": json.dumps(song_list)
        # 专辑
    }
    print("lyrics:", lyrics)
    return render(request, "user_front_page/online_songs/play_song.html", context)


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
            music_id=song,
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
    # 获取与特定用户相关的所有收藏音乐条目
    favorite_songs = MyFavoriteMusic.objects.filter(favorite_music_user_id=favorite_music_user_id)

    # 获取搜索查询参数
    search_query = request.GET.get('search', '')

    # 获取所有相关的 OnlineSongModel 实例，并根据搜索条件进行过滤
    all_songs = OnlineSongModel.objects.filter(
        id__in=favorite_songs.values_list('music_id', flat=True),
        song_title__icontains=search_query
    )
    paginator = Paginator(all_songs, per_page=20)  # 每页显示20条数据
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # 构建 song_list
    song_list = []
    for each_song in page_obj:
        song_list.append({
            "song_id": each_song.id,
            "song_title": each_song.song_title,
            "audio_file": each_song.audio_file.url,
            "song_author": each_song.song_author,
            "song_classification": each_song.song_classification
        })

    # 将结果渲染到模板中
    return render(request, 'user_front_page/online_songs/my_favorite_music.html',
                  {'page_obj': page_obj,
                   "songs_json": json.dumps(song_list),
                   "current_song_json": json.dumps(song_list[0]) if len(song_list) > 0 else {}})


@login_required
def delete_favorite_music(request, music_id):
    favorite_music = MyFavoriteMusic.objects.get(music_id=music_id)
    if request.method == 'POST':
        favorite_music.delete()
        return redirect('my_favorite_music_list', favorite_music_user_id=favorite_music.favorite_music_user_id.id)
    return render(request, 'user_front_page/online_songs/delete_favorite_music.html',
                  {'favorite_music': favorite_music})
