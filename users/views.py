from django.shortcuts import render, redirect
from . import models
from . import users_form
import datetime
from django.conf import settings
import hashlib
from django.http import JsonResponse


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def login(request):
    """
    登录视图
    :param request:
    :return:
    """
    # 不允许重复登录
    # if request.session.get("is_login", None):
    #     return redirect('/books/add/')
    if request.method == "POST":
        login_form = users_form.UserForm(request.POST)  # 把表单数据导入进来
        # POST会触发CSRF的防御机制，我们解决的第二种方案就是在html文件的form内部
        # 添加{% csrf_token %},可以在form表单的任意位置,在发送的时候，后台会自动过滤
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # 数据验证：分前端验证（这里利用的是H5的新特性帮助我们实现，字段不为空
        # 并且密码密文显示 ）和后端验证
        message = "请检查您输入的数据的格式!"
        # if username.strip() and password:    # 确保用户名和密码都不为空
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:  # try异常机制，防止数据库查询失败的异常
                # 首先验证该用户名在不在，存在返回对象，不存在直接回到登录页面
                user = models.User.objects.get(name=username)
            except:
                message = "用户不存在！"
                return render(request, 'login.html', locals())
            # if not user.has_confirmed:
            # 	message = '该用户还未经过邮件确认！'
            # 	return render(request, 'login.html', locals())
            if user.password == hash_code(password):
                # 往session字典内写入用户状态和数据
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/books')
            else:
                message = "密码不正确！"
                return render(request, 'users/login.html', locals())
        else:
            return render(request, 'users/login.html', locals())
    login_form = users_form.UserForm()
    return render(request, 'users/login.html', locals())


def register(request):
    """
    注册视图
    :param request:
    :return:
    """
    # if request.session.get('is_login', None):
    #     return redirect('/books/add/')

    if request.method == 'POST':
        register_form = users_form.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'users/register.html', locals())
            else:

                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'users/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'users/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
        else:
            return render(request, 'users/register.html', locals())
    register_form = users_form.RegisterForm()
    return render(request, 'users/register.html', locals())


def logout(request):
    """
    登出视图
    :param request:
    :return:
    """
    print(request.get_full_path())
    if not request.session.get('is_login', None):
        # 没有登录就没有登出之说
        return redirect('/login/')
    # 一次性将session中的所有内容全部清空
    request.session.flush()
    return redirect('/login/')
