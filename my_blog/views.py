# views.py

from django.shortcuts import render, redirect
from .models import BlogModel
from .forms import PostForm


def create_blog(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('create_blog', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'my_blog/create_blog.html', {'form': form})


def show_blog(request, pk):
    post = BlogModel.objects.get(pk=pk)
    return render(request, 'my_blog/show_blog.html', {'post': post})
