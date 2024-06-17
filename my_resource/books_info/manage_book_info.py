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


with open("offine_books_info.txt", 'r', encoding='utf-8') as fr:
    offline_books_info = fr.readlines()

all_book_image = []
for x in os.listdir("D:\program\python\library_manager_system-master\media\offline_book_images"):
    all_book_image.append(x.strip().split(".")[0])

books_path = "D:/tmp_file\google_download\ebook-master (1)\ebook-master"
count = 0
for x in os.listdir(books_path):
    book_name = x.split(".")[0].strip()
    if book_name in all_book_image:
        count += 1
        for each_book in offline_books_info:
            if each_book.strip().split(",")[0] == book_name:
                each_line = each_book.strip().split(",")[:3]
                each_line.extend([x, "小说"])
                # with open("online_book_info.txt", 'a', encoding='utf-8') as fr:
                #     fr.write(','.join(each_line) + '\n')
                shutil.copy(os.path.join(books_path,x),'D:\program\python\library_manager_system-master\media\online_books')
                continue

print(count)
# online_book_info = []
#
# for x in book_info:
#     if x.split(",")[0] in book_names.keys():
#         ks = x.split(",")[:3]
#         ks.append(book_names[x.split(",")[0]])
#         ks.append("小说")
#         online_book_info.append(",".join(ks))
#
# with open("online_book_info.txt", 'w', encoding='utf-8') as fw:
#     fw.writelines("\n".join(online_book_info))