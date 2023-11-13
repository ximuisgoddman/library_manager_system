from django.shortcuts import render
from .online_song_form import OnlineSongForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import OnlineSongModel
from django.contrib.auth.decorators import login_required
from myfavoritemusic.models import MyFavoriteMusic
from io import TextIOWrapper
from django.http import JsonResponse
import csv
import os
import json
from django.core.paginator import Paginator
from django.core.cache import cache


def upload_song(request):
    if request.method == 'POST':
        form = OnlineSongForm(request.POST, request.FILES)
        if form.is_valid():
            if 'file_upload' in request.FILES:
                # 处理文件上传逻辑
                file = request.FILES['file_upload']
                # 在这里解析文件数据并将数据写入数据库
                print("file:", file)
                songs_to_create = []
                file_wrapper = TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(file_wrapper)
                for row in reader:
                    song_filename = row[0].strip()
                    song_full_path = os.path.join('audio', song_filename)
                    song = OnlineSongModel(
                        song_author=row[1],
                        song_title=row[2],
                        audio_file=song_full_path,
                        song_duration=row[4],
                        song_classification=row[3]
                    )
                    OnlineSongModel.objects.bulk_create(songs_to_create)
                    songs_to_create.append(song)
                    # song.save()
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


def online_song_list(request):
    song_classifications = OnlineSongModel.objects.values_list('song_classification', flat=True).distinct()
    song_authors = OnlineSongModel.objects.values_list('song_author', flat=True).distinct()
    search_query = request.GET.get('search', '')
    cache_key = 'online_song_list_{}'.format(search_query)
    songs = cache.get(cache_key)
    if not songs:
        songs = OnlineSongModel.objects.all()
        cache.set(cache_key, songs, timeout=60 * 120)

    songs = songs.filter(song_title__icontains=search_query)
    song_author = request.GET.get('song_author', '')
    song_classification = request.GET.get('song_classification', '')
    songs = songs.filter(song_author__icontains=song_author)
    songs = songs.filter(song_classification__icontains=song_classification)
    song_list = []
    paginator = Paginator(songs, per_page=50)  # 每页显示10条数据
    page_number = request.GET.get('page')
    cache_key = 'song_list_page_info_{}'.format(search_query)
    page_obj = cache.get(cache_key)
    if not page_obj:
        page_obj = paginator.get_page(page_number)
        cache.set(cache_key, page_obj, timeout=60 * 10)
    for each_song in page_obj:
        song_list.append({"song_id": each_song.id,
                          "song_title": each_song.song_title.replace("'", " "),
                          "audio_file": each_song.audio_file.url.replace("'", " "),
                          "song_duration": each_song.song_duration.replace("'", " "),
                          "song_author": each_song.song_author.replace("'", " "),
                          "song_classification": each_song.song_classification.replace("'", " ")})
        each_song.song_format = each_song.audio_file.url.split(".")[-1].lower()

    return render(request, 'user_front_page/online_songs/song_list.html',
                  {'page_obj': page_obj,
                   'song_classifications': song_classifications,
                   'song_authors': song_authors,
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
