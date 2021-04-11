
from cmu_112_graphics import *
import json


def appStarted(self):
        self.typeCursor = True
        self.typeCursorFrame = 0
        self.typeCursorFrames = 4

        self.summonerName = ""
        self.error = None
        
        self.summonerInformation = None


def keyPressed(self, event):
    if len(event.key) == 1:
        self.summonerName += event.key
    elif event.key == 'Space':
        self.summonerName += " "
    elif event.key == "Backspace":
        length = len(self.summonerName)
        self.summonerName = self.summonerName[0:length-1]
    elif event.key == "Enter":
        if len(self.summonerName) > 0:
            if summonerNameValid(self):
                self.app.summonerInfo = self.summonerInformation
                self.summonerName = ""
                print(self.app.summonerInfo)
                self.app.setActiveMode(self.app.summonerInfoMode)

def summonerNameValid(self):

    # Try to load in any preexisting summoner information:
    fileName = "data/preexisting.txt"
    try:
        with open(fileName) as json_file:
            info = json.load(json_file)
    except:
        info = None
        raise ("preexisting data not found!")

    url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + self.summonerName + "?api_key=" + self.app.api
    summoner = requests.get(url)
    self.error = None
    if summoner.status_code == 403: # 4/10/21 so here we'd like to accomodate for non "404" errors by seeing if there's preexisting data in seach_screen. 
        print("API invalid")
        self.error = 403
        return False
    elif summoner.status_code == 404:
        print("Summoner name not found")
        self.error = 404
        return False
    elif summoner.status_code != 200:
        print("unknown error")
        return False
    self.summonerInformation = summoner.json()
    
    #rank information:
    url = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + self.summonerInformation['id'] + "?api_key=" + self.app.api
    temp = requests.get(url)
    if temp.status_code == 200:
        if temp.json() != []:
            self.summonerInformation['tier'] = temp.json()[0]['tier']  # Bronze
            self.summonerInformation['rank'] = temp.json()[0]['rank']  # I
        else:
            self.summonerInformation['tier'] = None
            self.summonerInformation['rank'] = None
    else:
        self.summonerInformation['tier'] = None
        self.summonerInformation['rank'] = None


    if (summoner_preexisting(self, info) == False):
        info.append(self.summonerInformation)
        with open(fileName, 'w') as outfile:
            json.dump(info, outfile, indent=4)

    return True


def summoner_preexisting(self, info):
    for summonerInfo in info:
        if (summonerInfo["name"].lower() == self.summonerName.lower()):
            return True
    return False

def timerFired(self):
    typingCursorSetting(self)

def typingCursorSetting(self):
    self.typeCursorFrame = (self.typeCursorFrame + 1) % self.typeCursorFrames
    if self.typeCursorFrame == 0:
        self.typeCursor = not self.typeCursor

def redrawAll(self, canvas):
    drawSearchScreen(self, canvas)
    

#code from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def drawSearchScreen(self, canvas):
    backgroundColor = rgbString(158, 189, 233)
    canvas.create_rectangle(0, 0, self.width, self.height, fill= backgroundColor)
    canvas.create_text(self.width//2, self.height//4, text="SummonerGUI", font = "arial 36 bold")

    #dimensions of the search box:
    w = self.width//3
    h = 80
    canvas.create_rectangle(self.width//2-w, self.height//2 - h, self.width//2+w, self.height//2, fill = "white", width = 0)
    champText = self.summonerName + "|" if self.typeCursor else self.summonerName

    if champText == "|" or champText == "":
        canvas.create_text(self.width//2 - w + 20, self.height//2-h + 25, text = "Enter Summoner Name.", anchor = 'nw', font = "helvetica 20", fill = "grey")

    canvas.create_text(self.width//2 - w + 20, self.height//2-h + 19, text=champText, font = "helvetica 24", anchor = 'nw')
    drawError(self, canvas, w, h)

def drawError(self, canvas, w, h):
    if self.error != None:
        if self.error == 403:
            canvas.create_text(self.width//2-w, self.height//2-h-17, text="Invalid API.", fill = "red", anchor = "w", font = "helvetica 12")
        elif self.error == 404:
            canvas.create_text(self.width//2-w, self.height//2-h-17, text="Summoner name not found", fill = "red", anchor = "w", font = "helvetica 12")
        else:
            canvas.create_text(self.width//2-w, self.height//2-h-17, text="Error, try again", fill = "red", anchor = "w", font = "helvetica 12")
