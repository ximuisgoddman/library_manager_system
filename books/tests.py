from django.test import TestCase

# Create your tests here.

with open('D:\my_program\py\library_manager_system/requirements.txt','r',encoding='utf-8') as fr:
    tmp=fr.readlines()

target=[]
for x in tmp:
    target.append(x.split(" ")[0]+"=="+x.split(" ")[-1])

with open('D:\my_program\py\library_manager_system/requirements.txt','w',encoding='utf-8') as fw:
    for x in target:
        fw.write(x)