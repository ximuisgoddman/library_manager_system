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

    # 保存歌词为LRC文件
    if lyrics_text:
        save_lyrics_as_lrc(save_path, artist, title, lyrics_text)
    if cover:
        save_cover_image(save_path, artist, title, cover)
    return {
        'album': album.text[0] if album else None,
        'title': title.text[0] if title else None,
        'artist': artist.text[0] if artist else None,
        'duration': duration
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

    # 保存歌词为LRC文件
    if lyrics_text:
        save_lyrics_as_lrc(save_path, artist, title, lyrics_text)
        # 保存封面图片
    if cover:
        save_cover_image(save_path, artist, title, cover)
    return {
        'album': album[0] if album else None,
        'title': title[0] if title else None,
        'artist': artist[0] if artist else None,
        'duration': duration
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

    # 保存歌词为LRC文件
    if lyrics_text:
        save_lyrics_as_lrc(save_path, artist, title, lyrics_text)
    if cover:
        save_cover_image(save_path, artist, title, cover)
    return {
        'album': album[0] if album else None,
        'title': title[0] if title else None,
        'artist': artist[0] if artist else None,
        'duration': duration
    }


def clean_filename(filename):
    """移除文件名中的无效字符"""
    return re.sub(r'[\/:*?"<>|]', '', filename)


def save_lyrics_as_lrc(file_path, artist, file_name, lyrics_text):
    """保存歌词为LRC文件"""
    file_name = "%s_%s" % (clean_filename(artist[0].strip()), clean_filename(file_name[0].strip())) + '.lrc'
    save_path = os.path.join(file_path, "online_songs", "lrc_file", file_name)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(lyrics_text)
    print(f"Lyrics saved to {file_name}")


def save_cover_image(file_path, artist, image_name, cover_data):
    """保存封面图片到本地"""
    # 尝试判断图像格式，默认保存为JPEG
    image_extension = '.jpg'
    # 如果cover_data是MP4格式的封面
    if isinstance(cover_data, list):
        cover_data = cover_data[0]
        if cover_data.imageformat == MP4Cover.FORMAT_PNG:
            image_extension = '.png'

    image_name = "%s_%s" % (clean_filename(artist[0].strip()), clean_filename(image_name[0].strip())) + image_extension
    with open(os.path.join(file_path, "online_songs", "image", image_name), 'wb') as img_file:
        img_file.write(cover_data)
    print(f"Cover image saved to {image_name}")


# print(extract_info("D:/ali_yun\music\chinese_music\陈奕迅_new/陈奕迅 - 16月6日晴.m4a",
#                    "D:/biancheng\python\library_manager_system\media"))

if __name__ == '__main__':
    my_path = "D:/ali_yun\music\chinese_music\陈奕迅_new"
    for x in os.listdir(my_path):
        extract_info(os.path.join(my_path, x), "D:/biancheng\python\library_manager_system\media")
