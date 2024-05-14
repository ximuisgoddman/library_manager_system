from django.shortcuts import render


def super_mario_bros(request):
    return render(request, 'super_mario/index.html')
