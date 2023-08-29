# encoding:utf-8
import os
import re
import shutil

# books_path = "D:/aliyun\来自分享\豆瓣读书TOP250(250册)"

# for x in os.listdir(books_path):
# if x.endswith("epub"):
#     shutil.copy(os.path.join(books_path,x),"D:/aliyun/epub")
# elif x.endswith("mobi"):
#     shutil.copy(os.path.join(books_path,x),"D:/aliyun/mobi")
# else:
#     print(x)
# for x in os.listdir(books_path):
# pattern = "(\d+)(.*)"
# ks = re.search(pattern, x).groups()
# new_name=x.replace(ks[0],"")
# os.rename(os.path.join(books_path,x),os.path.join(books_path,new_name))
# if x.startswith("."):
#     os.rename(os.path.join(books_path, x), os.path.join(books_path, x[1:]))

books_path = "D:/aliyun\epub"
book_names = {}
for x in os.listdir(books_path):
    book_name = x.split(".")[0].strip()
    book_names[book_name] = x

with open("offine_books_info.txt", 'r', encoding='utf-8') as fr:
    book_info = fr.readlines()
#
#
online_book_info = []

for x in book_info:
    if x.split(",")[0] in book_names.keys():
        ks = x.split(",")[:3]
        ks.append(book_names[x.split(",")[0]])
        ks.append("小说")
        online_book_info.append(",".join(ks))

with open("online_book_info.txt", 'w', encoding='utf-8') as fw:
    fw.writelines("\n".join(online_book_info))
