from django.db import models
from captcha.fields import CaptchaField
import hashlib
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from notifications.models import Notification
from django.urls import reverse


class MyUser(AbstractUser):
    """
    用户表
    """
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    create_time = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)
    # notifications = models.ManyToManyField('notifications.Notification')
    # 多对多关系，表示该用户关注了哪些用户
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')

    def get_absolute_url(self):
        print("@User")
        return reverse('article:user_article_list', args=[self.id])

    def get_unread_notifications(self):
        return Notification.objects.filter(recipient=self, unread=True)

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
        return self.password == hash_password

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-create_time']
