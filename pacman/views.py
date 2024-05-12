from django.shortcuts import render


def pacman(request):
    return render(request, 'pacman/index.html')
