# Generated by Django 3.2.16 on 2023-05-27 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyFavoriteMusic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('music_id', models.IntegerField()),
                ('song_title', models.CharField(max_length=100)),
                ('song_author', models.CharField(max_length=100)),
                ('song_classification', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('favorite_music_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_music_user_id', to='users.myuser')),
            ],
        ),
    ]
