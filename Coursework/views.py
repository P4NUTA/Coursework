import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm

Loginglobal = "none"
Passglobal = "none"
Funcglobal = "none"
Nameglobal = "none"


@csrf_exempt
def index(request):
    loginform = LoginForm()
    global Loginglobal
    global Passglobal
    global Funcglobal
    global Nameglobal
    if Loginglobal:
        if Funcglobal == "Admin":
            return redirect("/admin")
        elif Funcglobal == "Moderator":
            return redirect("/moderator")
        elif Funcglobal == "User":
            return redirect("/user")
    if request.POST:
        with open("Data/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.POST
        checkLogin = req.get("username")
        checkPass = req.get("password")
        checkFunc = "none"
        for i in users:
            if i["Login"] == checkLogin and i["Password"] == checkPass:
                checkFunc = i["Function"]
                Loginglobal = checkLogin
                Passglobal = checkPass
                Funcglobal = checkFunc
                Nameglobal = i["Name"]

                break
        if Loginglobal:
            if Funcglobal == "Admin":
                return redirect("/admin")
            elif Funcglobal == "Moderator":
                return redirect("/moderator")
            elif Funcglobal == "User":
                return redirect("/user")
    return render(request, 'index.html', {'form': loginform})


def adminrender(request):
    global Loginglobal
    global Passglobal
    global Funcglobal
    global Nameglobal

    if Funcglobal != "Admin":
        return redirect("/")

    return render(request, "menu_admin.html")


def moderatorrender(request):
    if Funcglobal != "Moderator":
        return redirect("/")
    return render(request, "menu_moderator.html")


def userrender(request):
    if Funcglobal != "User":
        return redirect("/")
    return render(request, "menu_user.html")


def indexhttp(request):
    return HttpResponse("123")


def handler404(request):
    response = render('404.html', context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render('500.html', context_instance=RequestContext(request))
    response.status_code = 404
    return response


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


def portlist(request):
    global Funcglobal
    if Funcglobal == "none":
        return redirect("/")
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Ports = data["Port"]
    return render(request, "portlist.html", {"Port": Ports, "Func": Funcglobal})


def portinfo(request, id):
    global Funcglobal
    if Funcglobal == "none":
        return redirect("/")
    id = id - 1
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Port = data["Port"][id]
    Docks = Port["Docks"]
    Workers = Port["Workers"]
    return render(request, "portinfo.html", {"Port": Port, "Docks": Docks, "Workers": Workers, "Func": Funcglobal})


def dockinfo(request, id, dock):
    global Funcglobal
    if Funcglobal == "none":
        return redirect("/")
    id = id - 1
    dock = dock - 1
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Port = data["Port"][id]
    Dock = Port["Docks"][dock]
    Ships = Dock["Ships"]
    return render(request, "dockinfo.html", {"Port": Port, "Dock": Dock, "Ships": Ships, "Func": Funcglobal})


@csrf_exempt
def adduser(request):
    global Funcglobal
    if Funcglobal != "Admin" and Funcglobal != "Moderator":
        return redirect("/")
    if request.POST:
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
    global Funcglobal
    if Funcglobal != "Admin":
        return redirect("/")
    if request.POST:
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
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Port = data
    id = id - 1
    if request.POST:
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

    return render(request, "adddock.html", {"Port": Port["Port"][id]})


@csrf_exempt
def addworker(request, id):
    id = id - 1
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Port = data
    if request.POST:
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

    return render(request, "addworker.html", {"Port": Port["Port"][id]})


def addship(request, id, dock):
    id = id - 1
    dock = dock - 1
    with open("Data/data.json", encoding='utf-8') as read_file_json:
        data = json.load(read_file_json)
    Port = data
    Dock = Port["Port"][id]["Docks"][dock]
    if request.POST:
        req = request.POST
        checkName = req.get("Name")
        checkType = req.get("Type")
        checkCharacteristic = req.get("Characteristic")
        checkTime = req.get("Time")
        checkTimeArrive = req.get("TimeArrive")
        ID = len(Port["Port"][id]["Docks"][dock]["Ships"]) + 1
        newship = {
            "ID": ID,
            "Name": checkName,
            "Type": checkType,
            "Work": True,
            "Characteristic": checkCharacteristic,
            "Time": checkTime,
            "TimeArrive": checkTimeArrive
        }
        data["Port"][id]["Docks"][dock]["Ships"].append(newship)
        with open('Data/data.json', 'w', encoding='utf-8') as read_file_json:
            read_file_json.write(json.dumps(data, ensure_ascii=False, separators=(',', ': '), indent=2))

    return render(request, "addship.html", {"Port": Port["Port"][id], "Dock": Dock})


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