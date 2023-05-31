from django.db import models
from users.models import MyUser


class MyFavoriteMusic(models.Model):
    music_id = models.IntegerField()
    audio_file = models.FileField()
    song_title = models.CharField(max_length=100)
    song_duration = models.CharField(max_length=100)
    song_author = models.CharField(max_length=100)
    song_classification = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    favorite_music_user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorite_music_user_id')

    def __str__(self):
        return str(self.favorite_music_user_id)