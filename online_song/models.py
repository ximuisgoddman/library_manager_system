from django.db import models
from users.models import MyUser


# Create your models here.
class OnlineSongModel(models.Model):
    song_image = models.ImageField(upload_to='online_songs/image/', max_length=500)
    song_title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='online_songs/audio/', max_length=500)
    lrc_file = models.FileField(upload_to='online_songs/lrc_file/', max_length=500)
    song_duration = models.CharField(max_length=100)
    song_author = models.CharField(max_length=100, db_index=True)
    song_classification = models.CharField(max_length=100, db_index=True)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)


class MyFavoriteMusic(models.Model):
    music_id = models.ForeignKey(OnlineSongModel, on_delete=models.CASCADE, related_name='favorite_music_id')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    favorite_music_user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorite_music_user_id')

    def __str__(self):
        return str(self.favorite_music_user_id)
