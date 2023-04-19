from django.db import models
from captcha.fields import CaptchaField
import hashlib
from django.contrib.auth.models import AbstractBaseUser


class AdminUser(AbstractBaseUser):
    """
    用户表
    """
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    USERNAME_FIELD = 'name'
    name = models.CharField(verbose_name="姓名", max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name='最后登录时间', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        # 简单地返回 True，表示该用户拥有所有权限
        return True

    def check_password(self, raw_password):
        """
        Validate the user's password.
        """
        # Your password hashing code goes here
        hash_password = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()
        print("check_password", self.password, hash_password, raw_password)
        return self.password == raw_password

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
