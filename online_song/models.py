from django.db import models


# Create your models here.
class OnlineSongModel(models.Model):
    song_title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio/')
    song_duration = models.CharField(max_length=100)
    song_author = models.CharField(max_length=100)
    song_classification = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
