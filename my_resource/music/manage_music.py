import random

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, USLT
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC
import os
import re
import shutil


def extract_info(file_path):
    # 获取文件的扩展名
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'mp3':
        return extract_mp3_info(file_path)
    elif file_extension in ['m4a', 'mp4']:
        return extract_mp4_info(file_path)
    elif file_extension == 'flac':
        return extract_flac_info(file_path)
    else:
        print(f"Unsupported file type: {file_extension}")
        return None


def extract_mp3_info(file_path):
    audio = MP3(file_path, ID3=ID3)

    album = audio.tags.get('TALB')
    duration = audio.info.length  # 获取时长

    # 修改：根据字段类型获取内容
    album_text = album.text[0] if album and hasattr(album, 'text') else album[0] if album else None
    return {
        'album': album_text,
        'duration': duration,
    }


def extract_mp4_info(file_path):
    audio = MP4(file_path)

    album = audio.tags.get('\xa9alb')
    duration = audio.info.length if audio.info else None  # 获取时长

    album_text = album[0] if album else None

    return {
        'album': album_text,
        'duration': duration,
    }


def extract_flac_info(file_path):
    audio = FLAC(file_path)
    album = audio.get('album')
    title = audio.get('title')
    artist = audio.get('artist')
    duration = audio.info.length  # 获取时长

    # 修改：根据字段类型获取内容
    album_text = album[0] if album else None
    title_text = title[0] if title else None
    artist_text = artist[0] if artist else None

    lrc_path, img_path = "", ""
    # 保存歌词为LRC文件
    return {
        'album': album_text,
        'title': title_text,
        'artist': artist_text,
        'duration': duration,
        'lrc_path': lrc_path,
        'img_path': img_path,
    }


# 示例调用
# if __name__ == '__main__':
#     chinese_music_file = "chinese_music.txt"
#     english_music_file = "english_music.txt"
#     with open(chinese_music_file, 'r', encoding='utf-8') as fr:
#         ch = fr.readlines()
#     with open(english_music_file, 'r', encoding='utf-8') as fr:
#         en = fr.readlines()
#     all_song = ch + en
#     random.shuffle(all_song)
#     with open('music.txt', 'w', encoding='utf-8') as fw:
#         fw.writelines(all_song)
# my_path = "D:/ali_yun\music\music_bak\chinese_music"
# for x in os.listdir(my_path):
#     music_info = extract_info(os.path.join(my_path, x))
#     for x in os.listdir(my_path):
#         for y in os.listdir(os.path.join(my_path, x)):
#             # shutil.copy(os.path.join(my_path, x, y), "D:/biancheng/english_music_audio")
#             # music_info = extract_info(os.path.join(my_path, x, y))
#             with open('chinese_music.txt', 'a', encoding='utf-8') as fw:
#                 artist, title = y.split(".")[0].split("-")[0].strip(), y.split(".")[0].split("-")[1].strip()
#                 fw.write("%s|%s|%s|%s|%s|%s|%s\n" % (
#                     artist, title,
#                     y, str(music_info['duration']).split(".")[0],
#                     music_info['album'],
#                     y.split(".")[0] + ".lrc",
#                     y.split(".")[0] + ".jpg"))

count=0
# my_path = "D:/ali_yun\music\music_bak\chinese_music"
# for x in os.listdir(my_path):
#     for y in os.listdir(os.path.join(my_path, x)):
#         count+=1
#         shutil.copy(os.path.join(my_path, x, y), "D:/biancheng\python\library_manager_system\media/bak/audio")
        # music_info = extract_info(os.path.join(my_path, x, y))
        # with open('english_music.txt', 'a', encoding='utf-8') as fw:
        #     try:
        #         artist, title = y[:-4].split("@")[0].strip(), y[:-4].split("@")[1].strip()
        #     except Exception as e:
        #         print(x,y)
        #     fw.write("%s|%s|%s|%s|%s|%s|%s\n" % (
        #         artist, title,
        #         y, str(music_info['duration']).split(".")[0],
        #         music_info['album'],
        #         y.split(".")[0] + ".lrc",
        #         y.split(".")[0] + ".jpg"))
#
print(count)

file1='chinese_music.txt'
file2='english_music.txt'
with open(file1,'r',encoding='utf-8') as fr:
    fr1=fr.readlines()

with open(file2,'r',encoding='utf-8') as fr:
    fr2=fr.readlines()

frr=fr1+fr2
random.shuffle(frr)
with open('music.txt','w',encoding='utf-8') as fw:
    fw.writelines(frr)

# count = 0
# testpath = "D:/ali_yun\music\music_bak"
# my_dic = {}
# for root, dirs, files in os.walk(testpath):
#     # print(root,dirs,files)
#     for name in files:
#         count += 1
#         print(os.path.join(root, name))
#         # shutil.copy(os.path.join(root, name), "D:/ali_yun\music/need_convert_format_new")
#
# print(count)
# for k,v in my_dic.items():
#     if len(v)>1:
#         print(v)
# os.remove(v[0])
# for x in v:
#     if not x.endswith(".mp3"):
#         print(x)
# os.remove(x)
