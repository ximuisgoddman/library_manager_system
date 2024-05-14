from django.shortcuts import render


def game2048(request):
    return render(request, 'game2048/index.html')
