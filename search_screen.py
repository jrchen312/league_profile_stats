
from cmu_112_graphics import *
import json

# API's used: 
#   SUMMONER-V4
#   LEAGUE-V4
# 


################################################################################
#
# App Started
def appStarted(self):
    self.typeCursor = True
    self.typeCursorFrame = 0
    self.typeCursorFrames = 4

    self.summonerName = ""
    self.reformattedSummonerName = ""   #self.summonerName in all lowercase. 
    self.error = None
    
    self.summonerInformation = None



################################################################################
#
# Key Pressed
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
            self.reformattedSummonerName = self.summonerName.lower()
            if summonerNameValid(self):
                self.app.summonerInfo = self.summonerInformation
                self.summonerName = ""
                print(self.app.summonerInfo)
                self.app.setActiveMode(self.app.summonerInfoMode)


# Uses SUMMONER-V4
# Uses LEAGUE-V4
def summonerNameValid(self):
    # Try to load in any preexisting summoner information:
    fileName = "data/preexisting.txt"
    try:
        with open(fileName) as json_file:
            preexisting = json.load(json_file)
            existing_summoner = summoner_preexisting(self, preexisting)
    except:
        #unsure if the above can ever throw an error. 
        with open(fileName, 'w') as json_file:
            json_file.write([])
        existing_summoner = None
        
    
    #API:
    s_url = ("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" 
                + self.reformattedSummonerName + "?api_key=" + self.app.api)
    s_request = requests.get(s_url)

    if s_request.status_code == 403: 
        print("API Invalid.")
        if existing_summoner == None:
            self.error = 403
            print("--Unable to find any preexisting information.")
            return False
        else: 
            self.summonerInformation = existing_summoner
    elif s_request.status_code == 404:
        print("Summoner name not found")
        self.error = 404
        return False
    elif s_request.status_code != 200:
        print("unknown error")
        return False
    else:  #s_request.status_code == 200
        # If we are logging the summoner in for the first time, do this:
        if existing_summoner == None:
            existing_summoner = s_request.json()
            existing_summoner['rank'] = None
            existing_summoner['tier'] = None
        rank = existing_summoner['rank']
        tier = existing_summoner['tier']

        self.summonerInformation = s_request.json()
        updateRanks(self, rank, tier)
    
    #reload the summoner information. 
    preexisting.append(self.summonerInformation)
    with open(fileName, 'w') as outfile:
        json.dump(preexisting, outfile, indent=4)

    return True


# Tries to update the ranks. If this does not work, then we try to maintain
# the old rank. 
def updateRanks(self, old_rank, old_tier):
    l_url = ("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" 
                + self.summonerInformation['id'] + "?api_key=" + self.app.api)
    l_request = requests.get(l_url)
    temp = l_request

    if temp.status_code == 200:
        if temp.json() != []:
            self.summonerInformation['tier'] = temp.json()[0]['tier']  # Bronze
            self.summonerInformation['rank'] = temp.json()[0]['rank']  # I
        else:
            self.summonerInformation['tier'] = None
            self.summonerInformation['rank'] = None
    else:
        print("Unable to update the ranks--trying to revert to old ranks")
        self.summonerInformation['tier'] = old_tier
        self.summonerInformation['rank'] = old_rank


# Checks the preexisting list and searches for the summoner name. 
# If this is found, the SummonerInfo is removed from the list. 
def summoner_preexisting(self, preexisting):
    for i in range(len(preexisting)):
        summonerInfo = preexisting[i]
        if (summonerInfo["name"].lower() == self.reformattedSummonerName):
            
            return preexisting.pop(i)
    return None


################################################################################
#
# TIMER FIRED
def timerFired(self):
    typingCursorSetting(self)

def typingCursorSetting(self):
    self.typeCursorFrame = (self.typeCursorFrame + 1) % self.typeCursorFrames
    if self.typeCursorFrame == 0:
        self.typeCursor = not self.typeCursor


################################################################################
#
# Redraw ALL
def redrawAll(self, canvas):
    drawSearchScreen(self, canvas)
    
#code from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def drawSearchScreen(self, canvas):
    backgroundColor = rgbString(158, 189, 233)
    canvas.create_rectangle(0, 0, self.width, self.height, fill=backgroundColor)
    canvas.create_text(self.width//2, self.height//4, 
                        text="SummonerGUI", font = "arial 36 bold")

    #dimensions of the search box:
    w = self.width//3
    h = 80
    canvas.create_rectangle(self.width//2-w, self.height//2-h, self.width//2+w, 
                            self.height//2, fill = "white", width = 0)
    champText = self.summonerName +"|" if self.typeCursor else self.summonerName

    if champText == "|" or champText == "":
        canvas.create_text(self.width//2 - w + 20, self.height//2-h + 25, 
                            text = "Enter Summoner Name.", fill = "grey",
                            anchor = 'nw', font = "helvetica 20")

    canvas.create_text(self.width//2 - w + 20, self.height//2-h + 19, 
                        text=champText, 
                        font = "helvetica 24", anchor = 'nw')
    drawError(self, canvas, w, h)

def drawError(self, canvas, w, h):
    if self.error != None:
        if self.error == 403:
            canvas.create_text(self.width//2-w, self.height//2-h-17, 
                                text="Invalid API.", fill = "red", 
                                anchor = "w", font = "helvetica 12")
        elif self.error == 404:
            canvas.create_text(self.width//2-w, self.height//2-h-17, 
                                text="Summoner name not found", fill = "red", 
                                anchor = "w", font = "helvetica 12")
        else:
            canvas.create_text(self.width//2-w, self.height//2-h-17, 
                                text="Error, try again", fill = "red", 
                                anchor = "w", font = "helvetica 12")
