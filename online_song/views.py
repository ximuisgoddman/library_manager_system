from django.shortcuts import render
from .online_song_form import OnlineSongForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import OnlineSongModel
from django.contrib.auth.decorators import login_required


def upload_song(request):
    form = OnlineSongForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('admin_online_song_list')
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
