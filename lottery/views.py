from django.shortcuts import render
import random  # 导入随机模块
import csv
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from io import TextIOWrapper

from .models import LotteryPrize
from .lottery_form import LotteryForm


def lottery_view(request):
    prizes = LotteryPrize.objects.all()  # 替换为您的奖品模型
    random_degree = random.randint(0, 359)  # 生成一个0到359之间的随机度数

    return render(request, "lottery/online_lottery.html", {
        "prizes": prizes,
        "random_degree": random_degree,
    })


@login_required
def upload_lottery_info(request):
    if not request.session.get("is_login", None):
        return redirect('/login/')
    if request.method == 'POST':
        form = LotteryForm(request.POST, request.FILES)
        if form.is_valid():
            if 'file_upload' in request.FILES:
                # 处理文件上传逻辑
                file = request.FILES['file_upload']
                # 在这里解析文件数据并将数据写入数据库
                print("file:", file)
                file_wrapper = TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(file_wrapper)
                for row in reader:
                    # 解析CSV文件内容并创建书籍对象
                    # book_image_path = row[7]
                    lottery_image_filename = row[0].strip() + '.jpg'
                    lottery_image_full_path = os.path.join('lottery_prizes/', lottery_image_filename)
                    lottery = LotteryPrize(
                        name=row[0],
                        percentage=row[1],
                        image=lottery_image_full_path  # 设置书籍图片路径
                    )
                    lottery.save()

                return redirect('book_list')
            else:
                book = form.save(commit=False)
                book.owner = request.user
                book.save()
                return redirect('book_list')
    else:
        form = LotteryForm()
    return render(request, 'lottery/lottery_upload.html', {'form': form})
