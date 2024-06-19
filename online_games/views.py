from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def online_games(request):
    return render(request, 'online_games/online_games.html')


def game2048(request):
    return render(request, 'game2048/index.html')


def sliding_puzzle(request):
    return render(request, 'sliding_puzzle/index.html')


def spaceship_shoot(request):
    return render(request, "spaceship_shoot/spaceship_shoot_v1.html")


def pacman(request):
    return render(request, 'pacman/index.html')


def super_mario_bros(request):
    return render(request, 'super_mario/index.html')


def snake(request):
    return render(request, "snake/snake_v1.html")


def tetris(request):
    return render(request, 'tetris_app/tetris.html')


def racing(request):
    return render(request, 'racing/index.html')


def minesweeper(request):
    return render(request, 'minesweeper/index.html')


def build_tower(request):
    return render(request, 'build_tower/index.html')


def cut_cubes(request):
    return render(request, 'cut_cubes/index.html')


def crossing_the_bridge(request):
    return render(request, 'crossing_the_bridge/index.html')


def breakthrough(request):
    return render(request, 'breakthrough/index.html')
