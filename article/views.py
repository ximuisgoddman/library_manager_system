# 引入redirect重定向模块
from django.shortcuts import render, redirect, get_object_or_404
# 引入User模型
from django.contrib.auth.models import User
# 引入HttpResponse
from django.http import HttpResponse
# 导入数据模型ArticlePost, ArticleColumn
from .models import ArticlePost, ArticleColumn
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入markdown模块
import markdown
# 引入login装饰器
from django.contrib.auth.decorators import login_required
# 引入分页模块
from django.core.paginator import Paginator
# 引入搜索 Q 对象
from django.db.models import Q
# Comment 模型
from comment.models import Comment

from comment.forms import CommentForm

# 通用类视图
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from users.models import MyUser
from .forms import MDEditorForm

# logging.config.dictConfig(LOGGING)
# logger = logging.getLogger('django.request')
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import time
import uuid

from django.http import JsonResponse, HttpResponse
from notifications.signals import notify


@csrf_exempt
def upload(request):
    obj = request.FILES.get('editormd-image-file')
    file_name = time.strftime('%Y%m%d%H%M%S') + str(uuid.uuid1().hex) + '.' + obj.name.split('.')[-1]
    dir_path = os.path.join(BASE_DIR, 'static', 'editor')
    img_path = os.path.join(dir_path, file_name)

    with open(img_path, 'wb') as f:
        for chunk in obj.chunks():
            f.write(chunk)

    response_data = {"success": 1, "message": "上传成功", "url": '/static/editor/' + file_name}
    response = JsonResponse(response_data)

    # 设置 X-Frame-Options 头，允许同域下的嵌套
    response['X-Frame-Options'] = 'SAMEORIGIN'

    return response


def demo(request):
    form = MDEditorForm()
    return render(request, 'mdeditor.html', {"form": form})


# 文章列表
def article_list(request):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        # 按热度排序博文
        article_list = article_list.order_by('-total_views')

    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


@login_required(login_url='login/')
def user_article_list(request, user_id):
    # 从 url 中提取查询参数
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = ArticlePost.objects.filter(author_id=user_id)
    article_author = MyUser.objects.filter(id=user_id).first()
    print("article_author:", article_author, article_author.username)
    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        # 按热度排序博文
        article_list = article_list.order_by('-total_views')

    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # 需要传递给模板（templates）的对象

    author_articles = ArticlePost.objects.filter(author_id=article_author)
    article_numbers = author_articles.count()
    author_likes = 0
    author_collects = 0
    author_views = 0
    author_followers = article_author.following.count()
    for each_article in author_articles:
        author_likes += each_article.likes
        author_collects += each_article.collects
        author_views += each_article.total_views
    context = {
        'author_followers': author_followers,
        'article_numbers': article_numbers,
        'author_likes': author_likes,
        'author_collects': author_collects,
        'author_views': author_views,
        'article_author': article_author,
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }
    # render函数：载入模板，并返回context对象
    return render(request, 'article/user_article_list.html', context)


# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    # article = ArticlePost.objects.get(id=id)
    # logger.warning('Something went wrong!')
    article = get_object_or_404(ArticlePost, id=id)

    # 取出文章评论
    comments = Comment.objects.filter(article=id)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # 相邻发表文章的快捷导航
    pre_article = ArticlePost.objects.filter(id__lt=article.id).order_by('-id')
    next_article = ArticlePost.objects.filter(id__gt=article.id).order_by('id')
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None

    # Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )
    article.content = md.convert(article.content)

    # 为评论引入表单
    comment_form = CommentForm()

    # 需要传递给模板的对象
    article_author = article.author
    author_articles = ArticlePost.objects.filter(author=article_author)
    article_numbers = author_articles.count()
    author_likes = 0
    author_collects = 0
    author_views = 0
    author_followers = article_author.following.count()
    for each_article in author_articles:
        author_likes += each_article.likes
        author_collects += each_article.collects
        author_views += each_article.total_views

    if_follow = article_author.following.filter(id=request.user.id).exists()
    print("if_follow:", if_follow)

    context = {
        'if_follow': if_follow,
        'author_followers': author_followers,
        'article_numbers': article_numbers,
        'author_likes': author_likes,
        'author_collects': author_collects,
        'author_views': author_views,
        'article': article,
        'toc': md.toc,
        'comments': comments,
        'pre_article': pre_article,
        'next_article': next_article,
        'comment_form': comment_form,
    }
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


# 写文章的视图
@login_required(login_url='login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定登录的用户为作者
            new_article.author = MyUser.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                # 保存文章栏目
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            # 保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 文章栏目
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)


# 删除文章，此方式有 csrf 攻击风险
@login_required(login_url='login/')
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")


# 安全删除文章
@login_required(login_url='login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权修改这篇文章。")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
@login_required(login_url='login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.content = request.POST['content']

            if request.POST['column'] != 'none':
                # 保存文章栏目
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            print("request.POST.get('tags'):", request.POST.get('tags'), len(request.POST.get('tags').split(',')))
            article.tags.set(request.POST.get('tags'), clear=True)
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()

        # 文章栏目
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': "".join(list(article.tags.names())),
        }

        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


# 点赞数 +1
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        print("IncreaseLikesView request.POST:", request.POST.get('like_status'))
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        if request.POST.get('like_status') == 'true':
            article.likes -= 1
            article.save()
            return HttpResponse('del_success')
        else:
            article.likes += 1
            article.save()
            return HttpResponse('add_success')


# 收藏数+1
class IncreaseCollectsView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        if request.POST.get('collect_status') == 'true':
            article.collects -= 1
            article.save()
            return HttpResponse('del_success')
        else:
            article.collects += 1
            article.save()
            return HttpResponse('add_success')


def article_list_example(request):
    """
    与下面的类视图做对比的函数
    简单的文章列表
    """
    if request.method == 'GET':
        articles = ArticlePost.objects.all()
        context = {'articles': articles}
        return render(request, 'article/list.html', context)


class ContextMixin:
    """
    Mixin
    """

    def get_context_data(self, **kwargs):
        # 获取原有的上下文
        context = super().get_context_data(**kwargs)
        # 增加新上下文
        context['order'] = 'total_views'
        return context


class ArticleListView(ContextMixin, ListView):
    """
    文章列表类视图
    """
    # 查询集的名称
    context_object_name = 'articles'
    # 模板
    template_name = 'article/list.html'

    def get_queryset(self):
        """
        查询集
        """
        queryset = ArticlePost.objects.filter(title='Python')
        return queryset


class ArticleDetailView(DetailView):
    """
    文章详情类视图
    """
    queryset = ArticlePost.objects.all()
    context_object_name = 'article'
    template_name = 'article/detail.html'

    def get_object(self):
        """
        获取需要展示的对象
        """
        # 首先调用父类的方法
        obj = super(ArticleDetailView, self).get_object()
        # 浏览量 +1
        obj.total_views += 1
        obj.save(update_fields=['total_views'])
        return obj


class ArticleCreateView(CreateView):
    """
    创建文章的类视图
    """
    model = ArticlePost
    fields = '__all__'
    # 或者有选择的提交字段，比如：
    # fields = ['title']
    template_name = 'article/create_by_class_view.html'


@login_required(login_url='login/')
def follow_user(request, author_id, article_id):
    article_author = get_object_or_404(MyUser, id=author_id)
    current_article = get_object_or_404(ArticlePost, id=article_id)
    # Check if the user is not already following
    if not article_author.following.filter(id=request.user.id).exists():
        article_author.following.add(request.user)

        notify.send(
            request.user,
            recipient=article_author,
            verb='关注了你',
            target=current_article,
        )
        return JsonResponse({'status': 'success', 'message': '关注成功'})
    else:
        notify.send(
            request.user,
            recipient=article_author,
            verb='取消关注了你',
            target=current_article,
        )
        article_author.following.remove(request.user)
        return JsonResponse({'status': 'error', 'message': '您已取消关注'})
