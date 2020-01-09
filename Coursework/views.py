import json
from http.client import HTTPResponse

from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseNotFound
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})


def error404(request):
    return Http404("123")

