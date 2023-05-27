from django.shortcuts import render
from myfavoritemusic.models import MyFavoriteMusic


def my_favorite_music_list(request):
    songs = MyFavoriteMusic.objects.all()
    search_query = request.GET.get('search', '')
    songs = songs.filter(song_title__icontains=search_query)
    return render(request, 'user_front_page/online_songs/my_favorite_music.html', {'songs': songs})
