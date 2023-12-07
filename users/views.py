import pdb

from django.shortcuts import render, redirect
from .models import MyUser
from . import users_form
from admin_users.admin_user_form import AdminUserForm
import datetime
from django.conf import settings
import hashlib
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from notifications.signals import notify
from django.contrib.auth.hashers import make_password, check_password

def hash_code(s, salt=''):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login


def my_login(request):
    """
    登录视图
    :param request:
    :return:
    """
    print("request.POST:", request.POST.get("user_type"))
    if request.method == "POST":
        if request.POST.get("user_type") == "normal":
            login_form = users_form.UserForm(request.POST)
            message = "请检查填写的内容！"
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                myuser = authenticate(username=username, password=password)
                if myuser is not None:
                    user_login(request, myuser)

                try:
                    # user = models.MyUser.objects.get(name=username)
                    # if not user.has_confirmed:
                    #     message = "该用户还未经过邮件确认！"
                    #     return render(request, 'general_users/login.html', locals())
                    # import pdb;pdb.set_trace()
                    print('PASSWORD', myuser.password, hash_code(password))
                    if myuser.password == hash_code(password):
                        # 设置session
                        request.session['is_login'] = True
                        request.session['user_id'] = myuser.id
                        request.session['user_name'] = myuser.username
                        # 设置重定向的URL
                        next_url = request.GET.get('next', None)
                        print("next_url:", next_url)
                        if next_url:
                            request.session['next_url'] = next_url
                        else:
                            request.session['next_url'] = reverse('home')
                        return redirect(request.session['next_url'])
                    else:
                        message = "密码不正确！"
                except:
                    message = "用户不存在！"
        elif request.POST.get("user_type") == "admin":
            login_form = users_form.UserForm(request.POST)
            message = "请检查填写的内容！"
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                myuser = authenticate(username=username, password=password)
                if myuser is not None:
                    user_login(request, myuser)

                try:
                    print('PASSWORD', myuser.password, hash_code(password), password)
                    if myuser.password == password:
                        # 设置session
                        request.session['is_login'] = True
                        request.session['user_id'] = myuser.id
                        request.session['user_name'] = myuser.username
                        # 设置重定向的URL
                        next_url = request.GET.get('next', None)
                        print("next_url:", next_url)
                        if next_url:
                            request.session['next_url'] = next_url
                        else:
                            request.session['next_url'] = reverse('book_list')
                        return redirect(request.session['next_url'])
                    else:
                        message = "密码不正确！"
                except:
                    message = "用户不存在！"
        return render(request, 'general_users/login.html', locals())
    login_form = users_form.UserForm()
    return render(request, 'general_users/login.html', locals())


def my_register(request):
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
                return render(request, 'general_users/register.html', locals())
            else:
                same_name_user = MyUser.objects.filter(username=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'general_users/register.html', locals())
                same_email_user = MyUser.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'general_users/register.html', locals())

                new_user = MyUser()
                new_user.username = username
                new_user.password = make_password(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
            return render(request, 'general_users/login.html', locals())
    return render(request, 'general_users/register.html', locals())


def logout(request):
    """
    登出视图
    :param request:
    :return:
    """
    print("path:", request.get_full_path())
    if not request.session.get('is_login', None):
        # 没有登录就没有登出之说
        return redirect('/login/')
    # 一次性将session中的所有内容全部清空
    request.session.flush()
    return redirect('/login/')


# 用户删除
# 验证用户是否登录的装饰器
@login_required(login_url='login/')
def user_delete(request, user_id):
    if request.method == 'POST':
        user = MyUser.objects.get(id=user_id)
        # 验证登录用户、待删除用户是否相同
        if request.user == user:
            # 退出登录，删除数据并返回博客列表
            user.delete()
            return redirect("/home")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("仅接受post请求。")


# 编辑用户信息
@login_required(login_url='login/')
def user_edit(request, user_id):
    user = MyUser.objects.get(id=user_id)
    # 旧教程代码
    # profile = Profile.objects.get(user_id=id)
    # 新教程代码： 获取 Profile
    if MyUser.objects.filter(id=user_id).exists():
        # user_id 是 OneToOneField 自动生成的字段
        profile = MyUser.objects.get(id=user_id)
    else:
        profile = MyUser.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        # 上传的文件保存在 request.FILES 中，通过参数传递给表单类
        profile_form = users_form.UserEditForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']

            # 如果 request.FILES 存在文件，则保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            # 构建重定向的 URL
            # return redirect(reverse('user_edit', kwargs={'user_id': user_id}))
            #   return redirect(f'/user_edit/{user_id}')
            return redirect('home')
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = users_form.UserForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'general_users/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")



