import os
from mutagen.mp3 import MP3
import re

mp3_file = "../../media/audio"
print(os.path.abspath(mp3_file))
for each_file in os.listdir(mp3_file):
    pattern = r"(.*?)\s-\s(.*?)\s\["
    author, song_name = re.search(pattern, each_file).groups()
    audio = MP3(os.path.join(mp3_file, each_file))
    try:
        zhuanji = audio["TALB"]
    except Exception:
        zhuanji = "--"
    timestamp = "%02d:%02d" %(int(audio.info.length)//60,int(audio.info.length)%60)
    with open("my_music.txt", 'a', encoding='utf-8') as fw:
        fw.write("%s,%s,%s,%s,%s\n" % (each_file, author, song_name, zhuanji, timestamp))
