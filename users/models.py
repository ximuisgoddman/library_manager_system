from django.db import models
from captcha.fields import CaptchaField


# Create your models here.
class User(models.Model):
    """
    用户表
    """
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = models.CharField(verbose_name="姓名", max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        """
        人性化显示对象信息
        :return:
        """
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = "用户"
        verbose_name_plural = "用户"

    '''
    注意：这里的用户名指的是网络上注册的用户名，不要等同于现实中的真实姓名，所以采用了唯一机制。
    如果是现实中的人名，那是可以重复的，肯定是不能设置unique的。另外关于密码，建议至少128位长度，原因后面解释。
    '''


class Author(models.Model):
    """
    作者表
    """
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    sex = models.CharField(max_length=16, choices=gender, default="男")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "作者表"
        verbose_name_plural = "作者表"
