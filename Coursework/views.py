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
    if Funcglobal == "none":
        return redirect("/")
    # Обработка страницы
    return render(request, "menu_admin.html")


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
    global Funcglobal
    if Funcglobal == "Admin":
        with open("Data/users.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        users = data["users"]
        listmoderators = []
        for i in users:
            if i["Function"] == "Moderator" and i["Work"]:
                listmoderators.append(i)
        return render(request, "moderatorlist.html", {"moderators": listmoderators})
    else:
        return redirect("/")


# Обработка страниц со списком пользователей
def userlist(request):
    global Funcglobal
    if Funcglobal == "Admin" or Funcglobal == "Moderator":
        with open("Data/users.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        users = data["users"]
        listusers = []
        for i in users:
            if i["Function"] == "User":
                listusers.append(i)
        return render(request, "userlist.html", {"users": listusers})
    else:
        return redirect("/")


# Обработка страниц со списком портов
def portlist(request):
    global Funcglobal
    if Funcglobal == "none":
        return redirect("/")
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Ports = data["Port"]
    return render(request, "portlist.html", {"Port": Ports})


# Вывод информации о порте
def portinfo(request, id):
    id = id - 1
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Port = data["Port"][id]
    Docks = Port["Docks"]
    Workers = Port["Workers"]
    return render(request, "portinfo.html", {"Port": Port, "Docks": Docks, "Workers": Workers})


# Обработка страниц со списком портов
def docklist(request, id):
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
        Dock = data["port"][id]
    return render(request, "docklist.html")


# Вывод информации о причале
def dockinfo(request, id, dock):
    id = id - 1
    dock = dock - 1
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Port = data["Port"][id]
    Dock = Port["Docks"][dock]
    Ships = Dock["Ships"]
    return render(request, "dockinfo.html", {"Dock": Dock, "Ships": Ships})


# Обработка страниц со списком портов
def shiplist(request):
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
        Ship = data["port"]
    return render(request, "shiplist.html")

@csrf_exempt
def adduser(request):
    if request.POST:
        with open("Data/users.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        users = data["users"]
        req = request.POST
        Name = req.get("Name")
        checkLogin = req.get("login")
        checkPass = req.get("password")
        checkFunc = req.get("function")
        checkerror = True
        for i in users:
            if checkLogin == i["login"]:
                print("Error")
                checkerror = False
                break
        if checkerror:
            ID = len(users) - 1
            newuser = {
                "Name": Name,
                "Login": checkLogin,
                "Password": checkPass,
                "ID": ID,
                "Work": True,
                "Function": checkFunc
            }
            users.append(newuser)
            with open('Data/users.json', 'w', encoding='utf-8') as read_file_json:
                read_file_json.write(json.dumps(users, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render (request,"adduser.html", {})