# __*__coding:utf-8__*__
from django import forms
from captcha.fields import CaptchaField
from .models import MyUser

'''
Django的表单给我们提供了下面三个主要功能：

准备和重构数据用于页面渲染；
为数据创建HTML表单元素；
接收和处理用户从表单发送过来的数据。
'''


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    captcha = CaptchaField(label="验证码")


class UserEditForm(forms.ModelForm):
    class Meta:
        model = MyUser
        # 定义表单包含的字段
        fields = ('phone', 'avatar', 'bio')


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ("female", "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')
