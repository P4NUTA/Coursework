import json

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm, AddUser

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
        for i in users:
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
            elif Funcglobal == "User":
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
    return render(request, "menu_moderator.html")


# Обработка страницы пользователя
def userrender(request):
    return render(request, "menu_user.html")


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
        users = data
        listmoderators = []
        for i in users:
            if i["Function"] == "Moderator" and i["Work"]:
                listmoderators.append(i)
        return render(request, "moderatorlist.html", {"moderators": listmoderators, "Func": Funcglobal})
    else:
        return redirect("/")


# Обработка страниц со списком пользователей
def userlist(request):
    global Funcglobal
    if Funcglobal == "Admin" or Funcglobal == "Moderator":
        with open("Data/users.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        users = data
        listusers = []
        for i in users:
            if i["Function"] == "User":
                listusers.append(i)
        return render(request, "userlist.html", {"users": listusers, "Func":Funcglobal})
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
    return render(request, "portlist.html", {"Port": Ports, "Func": Funcglobal})


# Вывод информации о порте
def portinfo(request, id):
    id = id - 1
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Port = data["Port"][id]
    Docks = Port["Docks"]
    Workers = Port["Workers"]
    return render(request, "portinfo.html", {"Port": Port, "Docks": Docks, "Workers": Workers, "Func":Funcglobal})



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


@csrf_exempt
def adduser(request):
    if request.POST:
        userform = AddUser()
        with open("Data/users.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        users = data
        req = request.POST
        Name = req.get("Name")
        checkLogin = req.get("Login")
        checkPass = req.get("Password")
        checkerror = True
        for i in users:
            if checkLogin == i["Login"]:
                print("Error")
                checkerror = False
                break
        if checkerror:
            ID = len(users) + 1
            newuser = {
                "Name": Name,
                "Login": checkLogin,
                "Password": checkPass,
                "ID": ID,
                "Work": True,
                "Function": "User"
            }
            users.append(newuser)
            with open('Data/users.json', 'w', encoding='utf-8') as read_file_json:
                read_file_json.write(json.dumps(users, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render(request, "adduser.html", {})


@csrf_exempt
def addmoderator(request):
    if request.POST:
        userform = AddUser()
        with open("Data/users.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        users = data
        req = request.POST
        Name = req.get("Name")
        checkLogin = req.get("Login")
        checkPass = req.get("Password")
        checkerror = True
        for i in users:
            if checkLogin == i["Login"]:
                print("Error")
                checkerror = False
                break
        if checkerror:
            ID = len(users) + 1
            newuser = {
                "Name": Name,
                "Login": checkLogin,
                "Password": checkPass,
                "ID": ID,
                "Work": True,
                "Function": "Moderator"
            }
            users.append(newuser)
            with open('Data/users.json', 'w', encoding='utf-8') as read_file_json:
                read_file_json.write(json.dumps(users, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render(request, "addmoderator.html", {})


def addport(request):
    if request.POST:
        with open("Data/data.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        Port = data
        req = request.POST
        checkName = req.get("Name")
        checkAddress = req.get("Address")
        checkTime = req.get("Time")
        checkerror = True
        for i in Port["Port"]:
            if checkName == i["Name"]:
                print("Error")
                checkerror = False
                break
        if checkerror:
            ID = len(Port["Port"]) + 1
            newPort = {
                "ID": ID,
                "Name": checkName,
                "Address": checkAddress,
                "Work": True,
                "Time": checkTime,
                "Docks": [],
                "Workers": []
            }
            data["Port"].append(newPort)
            with open('Data/data.json', 'w', encoding='utf-8') as read_file_json:
                read_file_json.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render(request, "addport.html", {})

def adddock(request, id):
    if request.POST:
        id = id-1
        with open("Data/data.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        Port = data
        req = request.POST
        checkName = req.get("Name")
        checkWorkNorm = req.get("WorkNorm")
        checkTime = req.get("WorkTime")
        checkType = req.get("Type")
        checkerror = True
        for i in Port["Port"][id]["Docks"]:
            if checkName == i["Name"]:
                print("Error")
                checkerror = False
                break
        if checkerror:
            ID = len(Port["Port"][id]["Docks"]) + 1
            newDock = {
                "ID": ID,
                "Name": checkName,
                "WorkNorm": checkWorkNorm,
                "WorkTime": checkTime,
                "Work": True,
                "Type": checkType,
                "Ships": []
            }
            data["Port"][id]["Docks"].append(newDock)
            with open('Data/data.json', 'w', encoding='utf-8') as read_file_json:
                read_file_json.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render(request, "adddock.html", {})

@csrf_exempt
def addworker(request, id):
    if request.POST:
        id = id - 1
        with open("Data/data.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        Port = data
        req = request.POST
        checkName = req.get("FIO")
        checkRole = req.get("Role")
        checkSalary = req.get("Salary")
        ID = len(Port["Port"][id]["Workers"]) + 1
        newWorker = {
            "FIO": checkName,
            "Role": checkRole,
            "ID": ID,
            "Work": True,
            "Salary": checkSalary,
        }
        data["Port"][id]["Workers"].append(newWorker)
        with open('Data/data.json', 'w', encoding='utf-8') as read_file_json:
            read_file_json.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render(request, "addworker.html", {})


def addship(request, id, dock_id):
    if request.POST:
        id = id - 1
        dock_id = dock_id - 1
        with open("Data/data.json", encoding='utf-8') as read_file_json:
            data = json.load(read_file_json)
        Port = data
        req = request.POST
        checkName = req.get("Name")
        checkType = req.get("Type")
        checkCharacteristic = req.get("Characteristic")
        checkTime = req.get("Time")
        ID = len(Port["Port"][id]["Workers"]) + 1
        newship = {
                "ID": 1,
                "Name": checkName,
                "Type": checkType,
                "Work": True,
                "Characteristic": "Science",
                "Time": "четверг 13:00"
            }
        data["Port"][id]["Workers"].append(newship)
        with open('Data/data.json', 'w', encoding='utf-8') as read_file_json:
            read_file_json.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render(request, "addworker.html", {})



def logout(request):
    global Loginglobal
    global Passglobal
    global Funcglobal
    global Nameglobal
    Loginglobal = "none"
    Passglobal = "none"
    Funcglobal = "none"
    Nameglobal = "none"
    return redirect("/")