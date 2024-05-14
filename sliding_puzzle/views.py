from django.shortcuts import render


def sliding_puzzle(request):
    return render(request, 'sliding_puzzle/index.html')
