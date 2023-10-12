from django.db import models
from users.models import MyUser


# Create your models here.
class LotteryPrize(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='lottery_prizes/')  # 存储奖品图片的字段
    percentage = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    # lottery_people = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='borrow_record')

    def __str__(self):
        return self.name
