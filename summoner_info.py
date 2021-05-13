#need to slim this down a ton. 
import json
import summoner_info_appstarted




def appStarted(self):
    summoner_info_appstarted.loadRanks(self)
    summoner_info_appstarted.loadSummonerSpells(self)
    summoner_info_appstarted.loadChampionDetails(self)
    summoner_info_appstarted.loadQueueDetails(self)

    #drawing stuff
    self.pageLeft = 220
    #button:
    self.buttonSize = (32, 108)
    self.buttonLocation = (self.pageLeft+10, 200)

    summoner_info_appstarted.summonerIconRank(self)
    summoner_info_appstarted.preexistingMatchHistoryInformation(self)
    summoner_info_appstarted.recentFifteenGames(self)

    self.updating = False
    self.preexisting = False
    self.matchIds = []
    self.currentMatchList = None
    self.i = 0
    self.j = 0
    self.progress = 0
    self.estimatedTime = 0

    self.mode = "overview" # "overview", "champions", "improvement"??
    self.modeButtonSize = (self.width-self.pageLeft*2)//3
    self.screenShift = 0
    self.scrolling = False
    self.initialScrollValue = 0

    self.gameStartIndex = 0
    self.numDisplayGames = 10
    minVal = len(self.matchHistory) if self.matchHistory != None else 0
    self.gameEndIndex = min(self.gameStartIndex + self.numDisplayGames, minVal)

    #loading information related to the champions--aggregate champion games and ranked stats: ('champions')
    self.sortingFactor = 'Games'
    self.descending = True
    summoner_info_appstarted.loadAggregateStats(self)
    summoner_info_appstarted.create_buttons(self)


# helper!
def sortDictionary(self, dictionary, para):
    dictContents = []
    for key in dictionary:
        temp = dict()
        temp[key] = dictionary[key]
        dictContents.append(temp)
    #return dictContents

    n = len(dictContents)
    for startIndex in range(n):
        minIndex = startIndex
        for i in range(startIndex+1, n):
            tempDict = dictContents[i]
            for key in tempDict:
                tempKey = key
            value1 = tempDict[tempKey][para]

            tempDict = dictContents[minIndex]
            for key in tempDict:
                tempKey = key
            value2 = tempDict[tempKey][para]
            if (value1 <= value2):
                minIndex = i
        swap(dictContents, startIndex, minIndex)
    return dictContents

#helper
def swap(a, i, j):
    (a[i], a[j]) = (a[j], a[i])





def mousePressed(self, event):
    buttonX, buttonY = self.buttonLocation
    dy, dx = self.buttonSize
    buttonX1, buttonY1 = buttonX + dx, buttonY + dy
    if buttonX <= event.x <= buttonX1 and buttonY <= event.y <= buttonY1:
        print('UPDATING')
        self.updating = True
        #getting the file name:
        file = self.summonerName.lower()
        for i in range(len(file)):
            if file[i] == " ":
                file = file[:i] + file[i+1:]
        fileName = file + 'Data.txt'
        try:
            with open(fileName) as json_file:
                self.preexisting = True
                print('file found!')
        except:
            self.preexisting = False
            print('no file found!')
    ##################################
    #Code for the mode buttons: pretty poor practice
    #button1 position:
    buttonSize = self.modeButtonSize
    x0, y0, x1, y1 = self.pageLeft, 290, self.pageLeft+buttonSize, 320
    #button2 position:
    x2, y2, x3, y3 = self.pageLeft+ buttonSize, 290, self.pageLeft+buttonSize * 2, 320
    #button3 pos:
    x4, y4, x5, y5 = self.pageLeft + buttonSize*2, 290, self.pageLeft+buttonSize*3, 320
    if x0 <= event.x <= x1 and y0 <= event.y <= y1:
        self.mode = "overview"
        self.screenShift = 0
    elif x2 <= event.x <= x3 and y2 <= event.y <= y3:
        self.mode = "champions"
        self.screenShift = 0
    elif x4 <= event.x <= x5 and y4 <= event.y <= y5:
        self.mode = "improvement"
        self.screenShift = 0
    
    ############
    # code for the buttons on the 'champions' screen
    if self.mode == 'champions':
        for button in self.buttons:
            result = button.pointInButton(event.x, event.y)
            if result != None and result != "Champion":
                if result == self.sortingFactor:
                    self.descending = not self.descending
                
                self.sortingFactor = result
                self.sortedAggregateStats = sortDictionary(self, self.championStats, self.sortingFactor)
                if self.descending:
                    self.sortedAggregateStats.reverse()
            #buttons:
            #['Games', 'Wins', 'Losses', 'Win Rate', 'Kills', 'Deaths', 'Assists', 'Damage', 'Dmg Taken', 'Vision', 'Gold', 'CS']
            # self.descending variable
    ###########
    # 
    if self.mode == 'overview':
        temp = inMatchButton(self, event.x, event.y)
        if temp != None:
            print(temp)
            self.app.currMatch = temp
            try:
                self.app.matchInfo = self.matchHistory[temp]
                self.app.setActiveMode(self.app.matchInfoMode)
            except:
                self.app.matchInfo = self.matchHistory[0]
            
            #now all we have to do is to go to the other screen, poggers!!! let's go!!!!!!!
    #################
    # scrolling?
    self.scrolling = True
    self.initialScrollValue = event.y

#move this before all of the user input! 
#by the way, this is an absolutely legnedary function, i believe i have peaked, god bless. 
def inMatchButton(self, x, y):
    start = 350
    size = 120
    buffer = 15
    buttonWidth = 50
    #change the x0 and x1 later. We need to draw a few buttons.. 
    x0 = self.width-(self.pageLeft + buttonWidth)
    x1 = self.width-self.pageLeft
    y0 = start
    y1 = self.height
    if x0 <= x <= x1 and y0 <= y <= y1:
        topIndex = self.screenShift//size
        topIndexPixels = self.screenShift%size
        y -= start

        tempY0 = buffer - topIndexPixels
        tempY1 = size - topIndexPixels
        i = 0
        while tempY1 < self.height:
            if tempY0 <= y <= tempY1:
                result = topIndex + i
                if result < len(self.matchHistory):
                    return (topIndex + i)
            i += 1
            tempY0 += size
            tempY1 += size
    return None


def mouseDragged(self, event):
    self.screenShift += (self.initialScrollValue - event.y) * 2
    self.initialScrollValue = event.y

def mouseReleased(self, event):
    self.scrolling = False #yeah, this is probably pretty useless lol
    #print(self.screenShift, self.gameStartIndex)


def keyPressed(self, event):
    if event.key == "Enter":
        pass

    elif event.key == "Down":
        self.screenShift += 25
    elif event.key == "Up":
        self.screenShift -= 25
    elif event.key == "Home":
        self.screenShift = 0
    elif event.key == "End":
        if self.matchHistory != None:
            self.screenShift = (len(self.matchHistory) - 4) * 120
            #120 is the 'size' of the buttons
    elif event.key == "Escape":
        MyModalApp.appStarted(self.app)
        #self.app.resetEverything = True
        #self.app.setActiveMode(app.searchScreenMode)


def matchIdLoader(self):
    url = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + self.app.summonerInfo['accountId'] + '?beginIndex=' + str(self.i) + '&api_key=' + self.app.api
    temp = requests.get(url)
    if temp.status_code == 200:

        matches = temp.json()
        for match in matches['matches']:
            self.matchIds.append(match)
        
        self.currentMatchList = matches # ['totalGames']
        self.i += 100

def team100team200Helper(self, participantStats):
    team100Stats = []
    team200Stats = []
    team100Kills = 0
    team200Kills = 0
    mostDmgDone = 0
    mostDmgTaken = 0
    for participantDict in participantStats:
        if participantDict['teamId'] == 100:
            team100Stats.append(participantDict)
            team100Kills += participantDict['stats']['kills']
        elif participantDict['teamId'] == 200:
            team200Stats.append(participantDict)
            team200Kills += participantDict['stats']['kills']
        if participantDict['stats']['totalDamageDealtToChampions'] > mostDmgDone:
            mostDmgDone = participantDict['stats']['totalDamageDealtToChampions']
        if participantDict['stats']['totalDamageTaken'] > mostDmgTaken:
            mostDmgTaken = participantDict['stats']['totalDamageTaken']
    
    team100 = {'players':team100Stats, 'kills':team100Kills}
    team200 = {'players':team200Stats, 'kills':team200Kills}
    gameWide = {'mostDmgDone': mostDmgDone, 'mostDmgTaken': mostDmgTaken}
    return team100, team200, gameWide

#helper function to get the rank (if there is one). 
def rankForJsonLoader(self, gameCreation):
    secondsInFiveDays = 432000
    if time.time() - secondsInFiveDays < gameCreation:
        rank = self.summonerRank
    else:
        rank = None
    return rank
    #1612032984 - 432000

def EPICGGSCORE(self):
    return None
    #lmao


def summonerIdTimeline(self, id, data):
    team100 = [1, 2, 3, 4, 5]
    team200 = [6, 7, 8, 9, 10]
    summonerId = id
    if summonerId <= 5:
        teamMates = team100
    else:
        teamMates = team200

    summonerFrames = []
    objectives = dict()
    kills, deaths, assists, dragons, heralds, barons, towers = 0, 0, 0, 0, 0, 0, 0
    skillLevelUps = []
    # -- 1: kills: 1, deaths: 2, assists: 3, 

    for minuteDictionary in data['frames']:
        zz = [ 'participantFrames (dict) ', 'events (list)', 'timestamp (milliseconds)']

        #declaration of a temp dictionary to store the results
        temp = dict()

        #checking events for kills/deaths/assists and objective takes by the summoner. 
        for event in minuteDictionary['events']:
            if event['type'] == 'SKILL_LEVEL_UP':
                if event['participantId'] == summonerId:
                    skillLevelUps.append(event['skillSlot'])
            elif event['type'] == 'CHAMPION_KILL':
                if event['victimId'] == summonerId:
                    deaths += 1
                elif event['killerId'] == summonerId:
                    kills += 1
                elif summonerId in event['assistingParticipantIds']:
                    assists += 1
            elif event['type'] == 'ELITE_MONSTER_KILL':
                if event['killerId'] in teamMates:
                    if event['monsterType'] == 'DRAGON':
                        dragons += 1
                    elif event['monsterType'] == 'RIFTHERALD':
                        heralds += 1
                    else:
                        barons += 1
            elif event['type'] == 'BUILDING_KILL':
                killers = event['assistingParticipantIds']
                killers.append(event['killerId'])
                if summonerId in killers:
                    towers += 1
            
        #getting the summonerId's game out of the participant frames. 
        for randomParticipant in minuteDictionary['participantFrames']:
            if minuteDictionary['participantFrames'][randomParticipant]['participantId'] == summonerId:
                temp['frame'] = minuteDictionary['participantFrames'][randomParticipant]
                temp['frame']['kills'] = kills
                temp['frame']['deaths'] = deaths
                temp['frame']['assists'] = assists
                temp['frame']['dragons'] = dragons
                temp['frame']['heralds'] = heralds
                temp['frame']['towers'] = towers
                temp['frame']['barons'] = barons
                break
        
        #minute in game, the key to the dictionary
        minute = minuteDictionary['timestamp']//60000
        temp['time'] = minute

        #append to the list
        summonerFrames.append(temp)

    return summonerFrames, skillLevelUps

def matchJsonLoader(self):
    match = self.matchIds[self.j]
    gameId = match['gameId']
    url = "https://na1.api.riotgames.com/lol/match/v4/matches/" + str(match['gameId']) + "?api_key=" + self.app.api
    v4Match = requests.get(url)
    url = 'https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/' + str(match['gameId']) + '?api_key=' +  self.app.api #timeline
    v4Timeline = requests.get(url) #timeline
    if v4Match.status_code == 200 and v4Timeline.status_code == 200:
        v4Match = v4Match.json()
        v4Timeline = v4Timeline.json() #timeline.
        participants = v4Match["participantIdentities"]
        participantIdOfSummoner = getParticipantIdOfSummoner(self, participants)
        participantStats = v4Match['participants']
        statsOfSummoner = None
        for participant in participantStats:
            if participant['participantId'] == participantIdOfSummoner:
                statsOfSummoner = participant
        team100, team200, gameWide = team100team200Helper(self, participantStats)
        rank = rankForJsonLoader(self, v4Match['gameCreation']//1000)
        timeline, skillOrder = summonerIdTimeline(self, participantIdOfSummoner, v4Timeline)
        self.matchIds[self.j]['gameDuration'] = v4Match['gameDuration'] #new addition
        self.matchIds[self.j]['rank'] = rank
        self.matchIds[self.j]['summonerStats'] = statsOfSummoner
        self.matchIds[self.j]['summonerStats']['skillOrder'] = skillOrder
        self.matchIds[self.j]['team100'] = team100
        self.matchIds[self.j]['team200'] = team200
        self.matchIds[self.j]['gameWide'] = gameWide
        self.matchIds[self.j]['participantIdentities'] = participants
        self.matchIds[self.j]['summonerIdTimeline'] = timeline
        self.matchIds[self.j]['EPICGGSCORE'] = self.EPICGGSCORE() #lmfao, 
        self.j += 1
        """
        'info already here'
        'gameDuration'
        'rank'
        'summonerStats' -- participant Id, teamId, summonerSpell, stats, timeline
        'team100' -- playerStats (list of 5 player stats), teamStats (numKills) 
        'team200' -- playerStats (participant 6-10), teamStats (numKills)
        'gameWide' -- mostDmgTaken, mostDmgDone,
        'participantIdentities'
        'summonerIdTimeline' -- "0": dictionaryOfStats
        """
    
    self.estimatedTime = int((len(self.matchIds) - self.j) * 2.2) #2.2 if using timeline, else, just 1.1
    self.progress = int(100 - (len(self.matchIds)-self.j)/(len(self.matchIds))*100)
    #print(f"Estimated Time remaining: {self.estimatedTime} seconds; progress: {self.progress}%")

def getParticipantIdOfSummoner(self, participants):
    for participant in participants:
        if participant['player']['currentAccountId'] == self.app.summonerInfo['accountId']:
            return participant['participantId']


def timerFired(self):
    if self.updating and not self.preexisting:
        updateController(self)
    elif self.updating and self.preexisting:
        updatePreexistingController(self)
    
    if self.mode == 'overview' and self.matchHistory != None:
        """
        self.gameStartIndex = 0
        self.numDisplayGames = 10
        minVal = len(self.matchHistory) if self.matchHistory != None else 0
        self.gameEndIndex = min(self.gameStartIndex + self.numDisplayGames, minVal)
        """
        start = 350
        size = 120
        buffer = 0
        
        temp = self.screenShift//(size + buffer)
        if temp < 0:
            temp = 0
        self.gameStartIndex = min(temp, len(self.matchHistory)-self.numDisplayGames)
        self.gameEndIndex = self.gameStartIndex + self.numDisplayGames

def updatePreexistingController(self):
    #populating the self.matchIds list
    if self.currentMatchList == None:
        matchIdLoader(self)
        #time of the most recent match
        self.mostRecentMatchDate = self.matchHistory[0]['timestamp']
        #toggle variable.
        self.matchIdsPrepared = False
    elif self.i < self.currentMatchList['totalGames']:
        matchIdLoader(self)
    else:
        if not self.matchIdsPrepared:
            print(len(self.matchIds))
            self.matchIdsPrepared = True
            temp = []
            for match in self.matchIds:
                if match['timestamp'] > self.mostRecentMatchDate:
                    temp.append(match)
            temp.reverse()
            self.matchIds = temp
            print(len(self.matchIds))
        elif self.j < len(self.matchIds):
            matchJsonLoader(self)
        else:
            self.updating = False
            #updating self.matchHistory
            for match in self.matchIds:
                self.matchHistory.insert(0, match)
            #file Name:
            file = self.summonerName.lower()
            for i in range(len(file)):
                if file[i] == " ":
                    file = file[:i] + file[i+1:]
            fileName = file + 'Data.txt'
            with open(fileName, 'w') as outfile:
                json.dump(self.matchHistory, outfile, indent=4)
            appStarted(self)

def updateController(self):
    if self.currentMatchList == None:
        matchIdLoader(self)
    elif self.i < self.currentMatchList['totalGames']:
        matchIdLoader(self)
    elif self.i >= self.currentMatchList['totalGames']:
        #need to start loading the match information, eventually storing it into a json file and restarting this app mode.
        #print(f"Number of matches: {len(self.matchIds)}")
        if self.j < len(self.matchIds):
            matchJsonLoader(self)
        else:
            self.updating = False
            file = self.summonerName.lower()
            for i in range(len(file)):
                if file[i] == " ":
                    file = file[:i] + file[i+1:]
            fileName = file + 'Data.txt'
            with open(fileName, 'w') as outfile:
                json.dump(self.matchIds, outfile, indent=4)
            appStarted(self)

def redrawAll(self, canvas):
    #Header:
    pageLeft = self.pageLeft #120???
    #page color:
    canvas.create_rectangle(pageLeft-20, 0, self.width-pageLeft+20, self.height, fill = "light blue", width = 0)

    #draw the mode:
    if self.mode == "overview":
        drawOverview(self, canvas)
    elif self.mode == "champions":
        drawChampions(self, canvas)
    elif self.mode == "improvement":
        drawImprovement(self, canvas)

    #draw a rectangle thing over the mode stuff to hide it :)
    canvas.create_rectangle(pageLeft-20, 0, self.width-pageLeft+20, 340, fill = "light blue", width = 0)
    #icon image:
    canvas.create_image(pageLeft, 50, image=ImageTk.PhotoImage(self.summonerIcon), anchor = 'nw')
    #summonerlevel?
    canvas.create_rectangle(pageLeft + 32, 160, pageLeft + 96, 190, fill='black' )
    canvas.create_text(pageLeft + 64, 175, text=str(self.summonerLevel), fill="white", font="arial 11 bold")
    #summoner name text
    canvas.create_text(pageLeft + 150, 60, text=self.summonerName, anchor = 'nw', font='arial 28 bold')
    #rank
    canvas.create_image(pageLeft + 140, 110, image=ImageTk.PhotoImage(self.rankIcons[self.summonerTier]), anchor = 'nw')
    canvas.create_text(pageLeft + 240, 150, text=self.summonerRank, font = 'arial 14', anchor='w')
    #canvas.create_text(pageLeft + 240, 170, text=self.summonerRank, font = 'arial 14', anchor='w')
    #button:
    x, y = self.buttonLocation
    dy, dx = self.buttonSize
    x1, y1 = x +dx, y + dy
    color = 'light green' if self.updating else 'green'
    canvas.create_rectangle(x, y, x1, y1, fill=color, width = 0)
    canvas.create_text(x + (x1-x)/2, y + (y1-y)/2, fill='white', text="Update", font = "Arial 12 bold")

    #line position:
    x10, y10, x11, y11 = self.pageLeft, 320, self.width-self.pageLeft, 320
    #button1 position:
    buttonSize = self.modeButtonSize
    x0, y0, x1, y1 = self.pageLeft, 290, self.pageLeft+buttonSize, 320
    #button2 position:
    x2, y2, x3, y3 = self.pageLeft+ buttonSize, 290, self.pageLeft+buttonSize * 2, 320
    #button3 pos:
    x4, y4, x5, y5 = self.pageLeft + buttonSize*2, 290, self.pageLeft+buttonSize*3, 320
    #buttons with the different modes: # "overview", "champions", "improvement"??
    canvas.create_line(x10, y10, x11, y11)
    color = "grey" if self.mode == "overview" else None
    canvas.create_rectangle(x0, y0, x1, y1, fill = color)
    canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2, text="Overview")
    color = "grey" if self.mode == "champions" else None
    canvas.create_rectangle(x2, y2, x3, y3, fill = color)
    canvas.create_text(x2+(x3-x2)/2, y2+(y3-y2)/2, text="Champions")
    color = "grey" if self.mode == "improvement" else None
    canvas.create_rectangle(x4, y4, x5, y5, fill = color)
    canvas.create_text(x4+(x5-x4)/2, y4+(y5-y4)/2, text="Improvement")

    
    #if we are updating, draw the progress bar
    if self.updating:
        length = 400
        x0, y0, x1, y1 = pageLeft+100, 240, pageLeft+100 + length, 265
        canvas.create_rectangle(x0, y0, x1, y1)

        ext = self.progress/100* length
        canvas.create_rectangle(x0, y0, x0 + ext, y1, fill = 'green', width = 0)
        
        canvas.create_text(x0, y0 + 35, text=f"{self.estimatedTime} seconds remaining", anchor='w')


    #trying to draw the champions last played in 15 games:
    x0, y0, x1, y1 = pageLeft+600, 40, pageLeft+ 838, 235
    canvas.create_rectangle(x0, y0, x1, y1)
    if self.fifteenStats == None:
        canvas.create_text(x0+(x1-x0)/2, y0+(y1-y0)/2, text="No Stats Found", font = "arial 20", fill = "grey")
    else:

        for i in range(len(self.fifteenStats)):
            dictionary = self.fifteenStats[i]
            for key in dictionary:
                pic = dictionary[key]['icon']
                x2 = x0 + 36
                y2 = y0 + 60 * i + 36
                canvas.create_image(x2, y2, image=ImageTk.PhotoImage(pic))

                #Draw champion name:
                x3 = x2 + 36
                y3 = y2 - 13
                canvas.create_text(x3, y3, text=key, anchor = "w")

                #Draw winrate and Wins/losses
                x4 = x3
                y4 = y3 + 24
                wins = dictionary[key]['wins']
                losses = dictionary[key]['losses']
                winRate = int((wins / dictionary[key]['games']) * 100)
                canvas.create_text(x4, y4, text=f"{winRate}%  ({wins}W {losses}L)", anchor = "w")

                #Draw the KDA
                x5 = x3 + 75
                y5 = y4
                killsAssists = dictionary[key]['kills'] + dictionary[key]['assists']
                deaths = dictionary[key]['deaths']
                kda = round(killsAssists/deaths, 2)
                canvas.create_text(x5, y5, text=f"{kda} KDA", anchor = "w")


def drawOverview(self, canvas):
    start = 350
    size = 120
    buffer = 15
    buttonWidth = 50
    #canvas.create_rectangle(self.pageLeft, start, self.width-self.pageLeft, start + size)
    #canvas.create_text(self.width/2, start + size/2, text='work in progress')
    shift = self.screenShift
    startY = start - shift
    #trying to list out the first 10 matches
    for i in range(self.gameStartIndex, self.gameEndIndex):
        matchDetails = self.matchHistory[i]
        if matchDetails['summonerStats']['stats']['win']:
            color = rgbString(97, 194, 75) #random green
            victoryText = "Win"
        else:
            color = rgbString(226, 182, 179) #soft red
            victoryText  = "Loss"
        x0 = self.pageLeft
        y0 = startY + (size)*i+buffer
        x1 = self.width-self.pageLeft
        y1 = startY + (size) * (i+1)
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        
        #queue !
        queue = self.queueToDescription[(matchDetails['queue'])]
        canvas.create_text(x0+40, y0 + size*(1/10), text=queue, font='calibri 10')

        min, sec = secondsToMinutes(matchDetails['gameDuration'])
        gameLength = f"{min}:{sec}"
        canvas.create_text(x0 + 40, y0 + size*(1/3), text=victoryText, font = 'calibri 14')
        canvas.create_text(x0 + 40, y0 + size*(2/3), text=gameLength, font = 'calibri 12')

        try:
            img1 = self.summonerSpellIcons[str(matchDetails['summonerStats']['spell1Id'])]
        except:
            img1 = self.summonerSpellIcons['0']
        try:
            img2 = self.summonerSpellIcons[str(matchDetails['summonerStats']['spell2Id'])]
        except:
            img2 = self.summonerSpellIcons['0']

        championPlayed = self.IDtoChampion[str(matchDetails['summonerStats']['championId'])]
        k = matchDetails['summonerStats']['stats']['kills']
        d = matchDetails['summonerStats']['stats']['deaths']
        a = matchDetails['summonerStats']['stats']['assists']

        kda = f"{k}/{d}/{a}"
        if d == 0:
            kd = f"KDA: {round(k+a, 2)}:1"
        else:
            kd = f"KDA: {round((k+a)/d, 2)}:1"
        canvas.create_text(x0 + 130, y0 + size*(2/5), text=championPlayed, font='calibri 18 bold')

        canvas.create_text(x0 + 300, y0 + size*(1/3), text=kda, font = 'calibri 12')
        canvas.create_text(x0 + 300, y0 + size*(2/3), text=kd, font = 'calibri 12')

        canvas.create_image(x0+220, y0 + size*(1/3)-5, image=ImageTk.PhotoImage(img1))
        canvas.create_image(x0+220, y0 + size*(2/3)-5, image=ImageTk.PhotoImage(img2))

        date = time.strftime('%m-%d-%Y', time.localtime(matchDetails['timestamp']//1000))
        t = time.strftime('%H:%M', time.localtime(matchDetails['timestamp']//1000))
        #date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(matchDetails['timestamp'])) #[:10]
        canvas.create_text(x1 - 140, y0 + size*(1/3), text=date, font='calibri 12')
        canvas.create_text(x1 - 140, y0 + size*(2/3), text=t, font='calibri 12')

        canvas.create_rectangle(x1 - buttonWidth, y0, x1, y1, fill = 'grey')
        x2, y2 = x1 - buttonWidth//2, y0 + size//2
        arrSize = 15
        canvas.create_line(x2 - arrSize, y2 - arrSize, x2, y2, width = 3)
        canvas.create_line(x2 + arrSize, y2 - arrSize, x2, y2, width = 3)

def secondsToMinutes(seconds):
    sec = seconds % 60
    min = seconds // 60
    return min, sec



def drawChampions(self, canvas):
    if self.aggregateGameStats == None:
        return
    start = 350+Button.ysize/2
    canvas.create_line(self.pageLeft, start, self.width-self.pageLeft, start)
    for button in self.buttons:
        button.draw(self, canvas)
    
    shift = self.screenShift
    y = start + Button.ysize - shift
    x = Button.xsize/2 + self.pageLeft
    k = 0 #k is the amount of vertical distance
    for dictionary in self.sortedAggregateStats:
        for key in dictionary:

            #does not display the champion if the number of games is less than 5. 
            if dictionary[key]['Games'] < 5:
                k-=1
                continue #?
            
            yTextPos = y+Button.ysize*(1+k)
            if yTextPos < start + Button.ysize/2:
                continue
            canvas.create_text(x, yTextPos, text=key)
            championStats = dictionary[key]
            i = 0 #i is the horizontal distance. 
            for key in championStats:
                if key == 'gameDuration': continue
                canvas.create_text(x+Button.xsize*(1+i), y+Button.ysize*(1+k), text=championStats[key])
                i += 1
        k += 1 




def drawImprovement(self, canvas):
    start = 350
    size = 120
    canvas.create_rectangle(self.pageLeft, start, self.width-self.pageLeft, start + size)
    canvas.create_text(self.width/2, start + size/2, text='work in progress')

#code from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

