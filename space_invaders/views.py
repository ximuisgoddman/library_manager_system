from django.shortcuts import render


def space_invaders(request):
    return render(request, 'space_invaders/index.html')