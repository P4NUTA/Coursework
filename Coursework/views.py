import json

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm


def index(request):
    login = LoginForm()
    # login = LoginForm(request.POST)
    return render(request, 'index.html', {'form': login})


def indexhttp(request):
    return HttpResponse("123")


def error404(request):
    return Http404("123")

# def get_name(request):
#     if request.method == 'POST':
#         form = Nameform(request.POST)
#         if form.is_valid():
#             return HttpResponse('/thanks/')
#     else:
#         form = Nameform()
#
#     return render(request, 'name.html', {'form': form})


# Reading data.json
with open("Data/data.json", 'rb') as read_file_json:
    data = json.load(read_file_json)

