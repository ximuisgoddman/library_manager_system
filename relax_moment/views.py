from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from myfavoritemusic.models import MyFavoriteMusic
from io import TextIOWrapper
from django.http import JsonResponse
import csv
import os
import json


def relax_moment(request):
    return render(request, 'relex_moment/relex_moment.html')
