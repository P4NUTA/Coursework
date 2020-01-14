import json

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm


# Обработка главной страницы
@csrf_exempt
def index(request):
    loginform = LoginForm()
    if request.POST:
        # Проверка входа в систему
        with open("Data/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.POST
        checkLogin = req.get("username")
        checkPass = req.get("password")
        checkFunc = "none"
        for i in users["users"]:
            if ('in' is request):
                break
            if i["Login"] == checkLogin and i["Password"] == checkPass:
                checkFunc = i["Function"]
                request.session.set_expiry(15)
                request.session['in'] = True
                request.session['login'] = i['login']
                request.session['Function'] = i['Function']
                break
        if request.session['Function'] == "Admin":
            return redirect("/admin")
        elif request.session['Function'] == "Moderator":
            return redirect("/moderator")
        elif request.session['Function'] == "user":
            return redirect("/user")
    return render(request, 'index.html', {'form': loginform})


# Обработка страницы админа
def adminrender(request):
    return render(request, "admin.html")


# Обработка страницы модератора
def moderatorrender(request):
    return render(request, "moderator.html")


# Обработка страницы пользователя
def userrender(request):
    return render(request, "user.html")


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
