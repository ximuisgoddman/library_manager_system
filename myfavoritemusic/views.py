from django.shortcuts import render
from myfavoritemusic.models import MyFavoriteMusic
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def my_favorite_music_list(request):
    songs = MyFavoriteMusic.objects.all()
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
        return redirect('my_favorite_music_list')
    return render(request, 'user_front_page/online_songs/delete_favorite_music.html', {'favorite_music': favorite_music})
