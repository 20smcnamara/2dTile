from django.http import HttpResponse

def index(request):
    return HttpResponse(getUpdatedInfo())

def players(request):

    return HttpResponse(getPlayerInfo())

def AddPlayer(request):
    text = ""
    with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Server\\Game\\GameData\\Players", 'r') as f:
        text = f.read()
    with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Server\\Game\\GameData\\Players", 'w') as f:
        f.write(text + 'p')
    return HttpResponse(len(text.split('p')) - 1)

def UpdatePlayer(request, x, y, id):
    text = ""
    with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Server\\Game\\GameData\\Players", 'r') as f:
        text = f.read()
    with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Server\\Game\\GameData\\Players", 'w') as f:
        newText = ""
        if id + 1 >= len(text.split("%")):
            newText = text + str(x) + "%" + str(y) + "p"
        else:
            for index, string in enumerate(text.split("p")):
                if string == "":
                    continue
                if index != id:
                    newText += string + "p"
                else:
                    newText += str(x) + "%" + str(y) + "p"
        f.write(newText)
    return HttpResponse(getPlayerInfo())

def RemovePlayer(request, x, y, id):
    text = ""
    with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Server\\Game\\GameData\\Players", 'r') as f:
        text = f.read()
    with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Server\\Game\\GameData\\Players", 'w') as f:
        newText = ""
        if id + 1 >= len(text.split("%")):
            newText = text + str(x) + "%" + str(y) + "p"
        else:
            for index, string in enumerate(text.split("p")):
                if string == "":
                    continue
                if index != id:
                    newText += string + "p"
        f.write(newText)
    return HttpResponse(getPlayerInfo())

def getPlayerInfo():
    with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Server\\Game\\GameData\\Players", "r") as f:
        contents = f.read()
    return contents

def getUpdatedInfo():
    with open("C:\\Users\\Sean\\PycharmProjects\\2dTile\\Server\\Game\\GameData\\Updates", "r") as f:
        contents = f.readline()
    return contents
