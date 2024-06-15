from django.shortcuts import render


def library_front_page(request):
    return render(request, 'user_front_page/front_page.html')
