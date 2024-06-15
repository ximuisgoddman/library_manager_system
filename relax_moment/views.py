from django.shortcuts import render


def relax_moment(request):
    return render(request, 'relex_moment/relex_moment.html')
