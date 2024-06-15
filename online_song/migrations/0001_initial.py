# Generated by Django 3.2.16 on 2024-06-15 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineSongModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_title', models.CharField(max_length=100)),
                ('audio_file', models.FileField(upload_to='audio/')),
                ('song_duration', models.CharField(max_length=100)),
                ('song_author', models.CharField(db_index=True, max_length=100)),
                ('song_classification', models.CharField(db_index=True, max_length=100)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyFavoriteMusic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_id', models.IntegerField()),
                ('audio_file', models.FileField(upload_to='')),
                ('song_title', models.CharField(max_length=100)),
                ('song_duration', models.CharField(max_length=100)),
                ('song_author', models.CharField(max_length=100)),
                ('song_classification', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('favorite_music_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_music_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
