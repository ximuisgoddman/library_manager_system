from django.shortcuts import render
from tetris_app.models import Game


# Create your views here.
def index(request):
    if request.method == 'GET':
        score = request.GET.get("score", None)
        if score != None:
            gameModel = Game(score=score)
            gameModel.save()
    gameInfo = Game.objects.all()[:10]

    return render(request, 'tetris_app/index.html', {'gameInfo': gameInfo})


def index1(request):
    return render(request, 'tetris_app/index1.html')


def canvas(request):
    return render(request, 'tetris_app/canvas.html')
