from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('index1/', index1, name='index1'),
    path('canvas/', canvas, name='canvas'),
    # path('/get', get_api),
    # path('/post', post_api),
]