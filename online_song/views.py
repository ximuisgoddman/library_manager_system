from django.shortcuts import render
from .online_song_form import OnlineSongForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import OnlineSongModel
from django.contrib.auth.decorators import login_required
from io import TextIOWrapper
import csv
import os


def upload_song(request):
    if request.method == 'POST':
        form = OnlineSongForm(request.POST, request.FILES)
        if form.is_valid():
            if 'file_upload' in request.FILES:
                # 处理文件上传逻辑
                file = request.FILES['file_upload']
                # 在这里解析文件数据并将数据写入数据库
                print("file:", file)
                file_wrapper = TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(file_wrapper)
                for row in reader:
                    song_filename = row[0].strip()
                    song_full_path = os.path.join('audio', song_filename)
                    song = OnlineSongModel(
                        song_title=row[2],
                        audio_file=song_full_path,
                        song_duration=row[3],
                        song_author=row[1],
                        song_classification=row[4]
                    )
                    song.save()
        else:
            song = form.save()
            song.save()
        return redirect('admin_online_song_list')
    else:
        form = OnlineSongForm()
    return render(request, 'online_song/upload_song.html', {'form': form})


def online_song_list(request):
    songs = OnlineSongModel.objects.all()
    return render(request, 'user_front_page/online_songs/song_list.html', {'songs': songs})


def admin_online_song_list(request):
    songs = OnlineSongModel.objects.all()
    return render(request, 'online_song/song_list.html', {'songs': songs})


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
