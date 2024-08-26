from django.shortcuts import render
import random  # 导入随机模块
import csv
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from io import TextIOWrapper

from .models import LotteryPrize
from .lottery_form import LotteryForm


import random
from django.shortcuts import render
from .models import LotteryPrize  # Ensure you have the correct import for your model

import random
from django.shortcuts import render
from .models import LotteryPrize


import random
from django.shortcuts import render
from .models import LotteryPrize

from django.shortcuts import render
import random

def lottery_view(request):
    prizes = LotteryPrize.objects.all()
    prize_count = len(prizes)  # 获取奖品数量
    random_degree = random.randint(0, 359)  # 生成一个0到359之间的随机度数

    # 计算每个奖品的角度
    prize_angles = []
    for i in range(prize_count):
        angle = i * 360 / prize_count
        prize_angles.append(angle)

    return render(request, "lottery/online_lottery.html", {
        "prizes": zip(prizes, prize_angles),
        "prize_count": prize_count,
        "random_degree": random_degree,
    })



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import csv
import os
from io import TextIOWrapper
from .models import LotteryPrize


@login_required
def upload_lottery_info(request):
    if request.method == 'POST':
        form = LotteryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('lottery_view')  # Redirect to a list or confirmation page
    else:
        form = LotteryForm()

    return render(request, 'lottery/lottery_upload.html', {'form': form})

