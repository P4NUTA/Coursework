import json

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm

# Глобальные переменные
Loginglobal = "none"
Passglobal = "none"
Funcglobal = "none"
Nameglobal = "none"
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

        global Loginglobal
        global Passglobal
        global Funcglobal
        global Nameglobal
        for i in users["users"]:
            if i["Login"] == checkLogin and i["Password"] == checkPass:
                checkFunc = i["Function"]
                Loginglobal = checkLogin
                Passglobal = checkPass
                Funcglobal = checkFunc
                Nameglobal = i["Name"]
                # request.session.set_expiry(15)
                # request.session['in'] = True
                # request.session['login'] = i['login']
                # request.session['Function'] = i['Function']
                break
        if checkFunc == "Admin":
            return redirect("/admin")
        elif checkFunc == "Moderator":
            return redirect("/moderator")
        elif checkFunc == "user":
            return redirect("/user")
    return render(request, 'index.html', {'form': loginform})


# Обработка страницы админа
def adminrender(request):
    if Loginglobal == "none":
        return redirect("/")
    with open("Data/data.json", 'rb') as read_file_json:
        data = json.load(read_file_json)
        Port = data["Port"]

    dict_port = {'Port': Port}
    return render(request, "admin.html", dict_port)


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
