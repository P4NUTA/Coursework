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
    # Форма входа
    loginform = LoginForm()

    # Подключение глобальных переменных
    global Loginglobal
    global Passglobal
    global Funcglobal
    global Nameglobal
    # Проверка логина
    if Loginglobal:
        if Funcglobal == "Admin":
            return redirect("/admin")
        elif Funcglobal == "Moderator":
            return redirect("/moderator")
        elif Funcglobal == "user":
            return redirect("/user")
    # Вход
    if request.POST:
        # Проверка входа в систему
        with open("Data/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.POST
        checkLogin = req.get("username")
        checkPass = req.get("password")
        checkFunc = "none"
        # Поиск пользователя
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
        # Быдло проверка входа
        if Loginglobal:
            if Funcglobal == "Admin":
                return redirect("/admin")
            elif Funcglobal == "Moderator":
                return redirect("/moderator")
            elif Funcglobal == "user":
                return redirect("/user")
    # Обработка страницы
    return render(request, 'index.html', {'form': loginform})


# Обработка страницы админа
def adminrender(request):
    # Подключение глобальных переменных
    global Loginglobal
    global Passglobal
    global Funcglobal
    global Nameglobal
    # Проверка залогинности
    if Loginglobal == "none":
        return redirect("/")
    # Обработка страницы
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


# Обработка страниц со списком модераторов
def moderatorlist(request):
    with open("Data/users.json") as read_file_json:
        users = json.load(read_file_json)
    return render(request, "moderatorlist.html")


# Обработка страниц со списком пользователей
def userlist(request):
    with open("Data/users.json") as read_file_json:
        users = json.load(read_file_json)
    return render(request, "userlist.html")


# Обработка страниц со списком портов
def portlist(request, ID):
    with open("Data/data.json") as read_file_json:
        data = json.load(read_file_json)
    Port = {}
    for i in data["Port"]:
        if i["ID"] == ID:
            Port = i
            break
    return render(request, "portlist.html", {'Port': Port})


# Обработка страниц со списком портов
def docklist(request, id):
    with open("Data/data.json") as read_file_json:
        data = json.load(read_file_json)
        Dock = data["port"][0]

    return render(request, "docklist.html")


# Обработка страниц со списком портов
def shiplist(request):
    with open("Data/data.json") as read_file_json:
        data = json.load(read_file_json)
        Ship = data["port"]
    return render(request, "shiplist.html")
