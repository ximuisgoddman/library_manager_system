import os
import shutil

from mutagen.mp3 import MP3
import re

import wave

from mutagen.flac import FLAC

from mutagen.mp4 import MP4


def get_m4a_duration(file_path):
    try:
        audio = MP4(file_path)
        duration = audio.info.length
        return duration
    except Exception as e:
        print("Error while getting duration:", e)
        return None


def get_flac_duration(file_path):
    try:
        audio = FLAC(file_path)
        duration = audio.info.length
        return duration
    except Exception as e:
        print("Error while getting duration:", e)
        return None


def get_wav_duration(file_path):
    try:
        with wave.open(file_path, 'rb') as wav_file:
            # 获取音频的帧率（每秒的采样数）
            frame_rate = wav_file.getframerate()

            # 获取音频的总帧数
            num_frames = wav_file.getnframes()

            # 计算音频时长（秒）
            duration = num_frames / float(frame_rate)

            return duration
    except wave.Error as e:
        print("Error reading WAV file:", e)
        return None


def get_music_info(music_path):
    count = 0
    for x in os.listdir(music_path):
        if x.endswith(".git"):
            continue
        for each_file in os.listdir(os.path.join(music_path, x)):
            author, song_name, zhuanji, timestamp = "", "", "", ""
            try:
                author, song_name = each_file.split(".")[0].split("-")
            except Exception as e:
                print(os.path.join(music_path, x, each_file), e)
            if each_file.endswith(".mp3"):
                try:
                    audio = MP3(os.path.join(music_path, x, each_file))
                    # zhuanji = audio["TALB"]
                    timestamp = "%02d:%02d" % (int(audio.info.length) // 60, int(audio.info.length) % 60)

                except Exception as e:
                    print(os.path.join(music_path, x, each_file), e)
                    zhuanji = "--"

            if each_file.endswith(".wav"):
                duration = get_wav_duration(os.path.join(music_path, x, each_file))
                if duration is not None:
                    timestamp = "%02d:%02d" % (int(duration) // 60, int(duration) % 60)
                    # shutil.copy(os.path.join(music_path, x, each_file), "D:\my_program\py\library_manager\media\\audio")
                    # count+=1
                    # with open("my_music2.txt", 'a', encoding='utf-8') as fw:
                    #     fw.write(
                    #         "%s,%s,%s,%s,%s\n" % (each_file, author.strip(), song_name.strip(), zhuanji, timestamp))
            #
            #         if count>20:
            #             break
            #     else:
            #         print("无法获取音频时长。", each_file)

            if each_file.endswith(".flac"):
                duration = get_flac_duration(os.path.join(music_path, x, each_file))
                if duration is not None:
                    timestamp = "%02d:%02d" % (int(duration) // 60, int(duration) % 60)
            #         shutil.copy(os.path.join(music_path, x, each_file), "D:\my_program\py\library_manager\media\\audio")
            #         count+=1
            #         with open("my_music2.txt", 'a', encoding='utf-8') as fw:
            #             fw.write(
            #                 "%s,%s,%s,%s,%s\n" % (each_file, author.strip(), song_name.strip(), zhuanji, timestamp))
            #
            #         if count>20:
            #             break
            #     else:
            #         print("无法获取音频时长。", each_file)
            elif each_file.endswith(".m4a"):
                duration = get_m4a_duration(os.path.join(music_path, x, each_file))
                if duration is not None:
                    timestamp = "%02d:%02d" % (int(duration) // 60, int(duration) % 60)
            # else:
            #     print("Error format", os.path.join(music_path, x, each_file))
            shutil.copy(os.path.join(music_path, x, each_file), "D:\my_program\py\library_manager_system-master\media/audio")
            with open("my_music2.txt", 'a', encoding='utf-8') as fw:
                fw.write(
                    "%s,%s,%s,%s,%s\n" % (
                    each_file, author.strip(), song_name.strip(),
                    zhuanji, timestamp))


get_music_info("D:\BaiduNetdiskDownload\music")

# music_path = "D:\BaiduNetdiskDownload\music\吴青峰"
# for x in os.listdir(music_path):
#     # print(x.split(".")[0])
#     if "吴青峰" in x.split(".")[0].split("-")[1]:
#         # print(x)
#         os.rename(os.path.join(music_path, x), os.path.join(music_path, "%s-%s.%s" % (
#         x.split("-")[1].split(".")[0].strip(), x.split("-")[0].strip(), x.split(".")[-1])))
# if "苏打绿" not in x:
#     os.rename(os.path.join(music_path, x), os.path.join(music_path, "苏打绿-%s" %x))
# else:
#     os.rename(os.path.join(music_path, x), os.path.join(music_path, "%s-%s.%s"%(x.split("-")[1].split(".")[0].strip(),x.split("-")[0].strip(),x.split(".")[-1])))


#
music_path = "D:\my_program\py\library_manager_system-master\media"
count = 0
for x in os.listdir(music_path):
    for y in os.listdir(os.path.join(music_path, x)):
        if x.endswith(".git"):
            continue

        try:
            count += 1
            # author,name=y.split(".")[0].split("-")
            # if "," in author or x in name:
            #     os.rename(os.path.join(music_path,x,y),os.path.join(music_path,x,y.replace(",","&")))

        except Exception as e:
            print(x, y, e)
print(count)
