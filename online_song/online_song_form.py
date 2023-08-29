from django import forms
from .models import OnlineSongModel


class OnlineSongForm(forms.ModelForm):
    file_upload = forms.FileField(required=False)
    class Meta:
        model = OnlineSongModel

        fields = ('song_title', 'audio_file', 'song_duration', 'song_author', 'song_classification')
        labels = {
            'song_title': "歌名",
            'audio_file': "音乐文件",
            'song_duration': "音乐时长",
            'song_author': "作曲",
            'song_classification': "分类"
        }
