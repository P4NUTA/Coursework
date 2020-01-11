import json

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm


@csrf_exempt
def index(request):
    loginform = LoginForm()
    page = 'index.html'
    if request.GET:
        with open("Data/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.GET
        # Проверка входа в систему
        checkLogin = req.get("username")
        checkPass = req.get("password")
        checkFunc = "none"
        for i in users["users"]:
            if i["Login"] == checkLogin and i["Password"] == checkPass:
                checkFunc = i["Function"]
            if checkFunc == "Admin":
                page = "admin.html"
                break
            elif checkFunc == "Moderator":
                page = "moderator.html"
                break
            elif checkFunc == "user":
                page = "user.html"
                break
    return render(request, page, {'form': loginform})


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

