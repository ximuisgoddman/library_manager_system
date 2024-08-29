from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, USLT
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC
import os
import re


def extract_info(file_path, save_path):
    # 获取文件的扩展名
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'mp3':
        return extract_mp3_info(file_path, save_path)
    elif file_extension in ['m4a', 'mp4']:
        return extract_mp4_info(file_path, save_path)
    elif file_extension == 'flac':
        return extract_flac_info(file_path, save_path)
    else:
        print(f"Unsupported file type: {file_extension}")
        return None


def extract_mp3_info(file_path, save_path):
    audio = MP3(file_path, ID3=ID3)

    album = audio.tags.get('TALB')
    title = audio.tags.get('TIT2')
    artist = audio.tags.get('TPE1')
    lyrics = audio.tags.get('USLT')  # Unsynchronized lyrics/text transcription frame
    duration = audio.info.length  # 获取时长

    cover = None
    for tag in audio.tags.values():
        if isinstance(tag, APIC):
            cover = tag.data
            break

    lyrics_text = None
    if lyrics:
        try:
            lyrics_text = lyrics.text if isinstance(lyrics, USLT) else lyrics
        except Exception as e:
            print("Failed to decode lyrics:", e)

    # 修改：根据字段类型获取内容
    album_text = album.text[0] if album and hasattr(album, 'text') else album[0] if album else None
    title_text = title.text[0] if title and hasattr(title, 'text') else title[0] if title else None
    artist_text = artist.text[0] if artist and hasattr(artist, 'text') else artist[0] if artist else None

    lrc_path, img_path = "", ""
    # 保存歌词为LRC文件
    if lyrics_text:
        lrc_path = save_lyrics_as_lrc(save_path, artist_text, title_text, lyrics_text)
    if cover:
        img_path = save_cover_image(save_path, artist_text, title_text, cover)
    return {
        'album': album_text,
        'title': title_text,
        'artist': artist_text,
        'duration': duration,
        'lrc_path': lrc_path,
        'img_path': img_path,
    }


def extract_mp4_info(file_path, save_path):
    audio = MP4(file_path)

    album = audio.tags.get('\xa9alb')
    title = audio.tags.get('\xa9nam')
    artist = audio.tags.get('\xa9ART')
    lyrics = audio.tags.get('\xa9lyr')
    duration = audio.info.length if audio.info else None  # 获取时长
    cover = None
    if 'covr' in audio.tags:
        cover = audio.tags['covr'][0]

    lyrics_text = lyrics[0] if lyrics else None

    # 修改：根据字段类型获取内容
    album_text = album[0] if album else None
    title_text = title[0] if title else None
    artist_text = artist[0] if artist else None

    lrc_path, img_path = "", ""
    # 保存歌词为LRC文件
    if lyrics_text:
        lrc_path = save_lyrics_as_lrc(save_path, artist_text, title_text, lyrics_text)
    if cover:
        img_path = save_cover_image(save_path, artist_text, title_text, cover)
    return {
        'album': album_text,
        'title': title_text,
        'artist': artist_text,
        'duration': duration,
        'lrc_path': lrc_path,
        'img_path': img_path,
    }


def extract_flac_info(file_path, save_path):
    audio = FLAC(file_path)

    album = audio.get('album')
    title = audio.get('title')
    artist = audio.get('artist')
    lyrics = audio.get('lyrics')
    duration = audio.info.length  # 获取时长

    cover = None
    if audio.pictures:
        cover = audio.pictures[0].data

    lyrics_text = lyrics[0] if lyrics else None

    # 修改：根据字段类型获取内容
    album_text = album[0] if album else None
    title_text = title[0] if title else None
    artist_text = artist[0] if artist else None

    lrc_path, img_path = "", ""
    # 保存歌词为LRC文件
    if lyrics_text:
        lrc_path = save_lyrics_as_lrc(save_path, artist_text, title_text, lyrics_text)
    if cover:
        img_path = save_cover_image(save_path, artist_text, title_text, cover)
    return {
        'album': album_text,
        'title': title_text,
        'artist': artist_text,
        'duration': duration,
        'lrc_path': lrc_path,
        'img_path': img_path,
    }


def clean_filename(filename):
    """移除文件名中的无效字符"""
    return re.sub(r'[\/:*?"<>|]', '', filename)


def save_lyrics_as_lrc(file_path, artist, file_name, lyrics_text):
    """保存歌词为LRC文件"""
    file_name = "%s_%s" % (clean_filename(artist.strip()), clean_filename(file_name.strip())) + '.lrc'
    save_path = os.path.join(file_path, "online_songs", "lrc_file", file_name)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(lyrics_text)
    return file_name


def save_cover_image(file_path, artist, image_name, cover_data):
    """保存封面图片到本地"""
    # 尝试判断图像格式，默认保存为JPEG
    image_extension = '.jpg'
    # 如果cover_data是MP4格式的封面
    if isinstance(cover_data, list):
        cover_data = cover_data[0]
        if cover_data.imageformat == MP4Cover.FORMAT_PNG:
            image_extension = '.png'

    image_name = "%s_%s" % (clean_filename(artist.strip()), clean_filename(image_name.strip())) + image_extension
    with open(os.path.join(file_path, "online_songs", "image", image_name), 'wb') as img_file:
        img_file.write(cover_data)
    return image_name


# 示例调用
if __name__ == '__main__':
    music_file = "my_music.txt"
    my_path = "D:/ali_yun/music/chinese_music/陈奕迅_new"
    for x in os.listdir(my_path):
        music_info = extract_info(os.path.join(my_path, x), "D:/biancheng/python/library_manager_system/media")
        with open(music_file, 'a', encoding='utf-8') as fw:
            fw.write("%s|%s|%s|%s|%s|%s|%s\n" % (
                music_info['artist'], music_info['title'],
                x, music_info['duration'],
                music_info['album'],
                music_info['lrc_path'], music_info['img_path']))
