#need to slim this down a ton.
import json
import requests
import time
import summoner_info_appstarted
import summoner_info_redrawall
import button



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
    self.matchListLength #NOTE: this is the new method. 
    self.i = 0
    self.j = 0
    self.progress = 0
    self.estimatedTime = 0

    self.mode = "overview" # "overview", "champions", "improvement"??
    self.modeButtonSize = (self.width-self.pageLeft*2)//3
    self.screenShift = 0
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




################################################################################
#
# User input
def mousePressed(self, event):
    buttonX, buttonY = self.buttonLocation
    dy, dx = self.buttonSize
    buttonX1, buttonY1 = buttonX + dx, buttonY + dy
    if buttonX <= event.x <= buttonX1 and buttonY <= event.y <= buttonY1:
        print('UPDATING')
        self.updating = True
        #getting the file name:
        fileName = self.app.summonerInfo['accountId']
        #file = self.summonerName.lower()
        #for i in range(len(file)):
        #    if file[i] == " ":
        #        file = file[:i] + file[i+1:]
        #fileName = file + 'Data.txt'
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
            

    #################
    # scrolling?
    self.initialScrollValue = event.y

#move this before all of the user input! 
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



################################################################################
#
# Timer Fired


#Grabs the next 100 matches from the account's matchlist. 
# matchv4   matchlist (depreciated 6/26/2021)

def matchIdLoader(self):
    #url = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + self.app.summonerInfo['accountId'] + '?beginIndex=' + str(self.i) + '&api_key=' + self.app.api
    v5_url = ("https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + 
            self.app.summonerInfo['puuid'] + '/ids?start=' + str(self.i) + 
            '&count=' + (str(100)) + '&api_key=' + self.app.api)
    temp = requests.get(v5_url)
    if temp.status_code == 200:

        matches = temp.json()  #"matches" to a list of matchIds.
        for match in matches:
            storage = dict()
            storage['gameId'] = match;
            self.matchIds.append(storage)
        
        #NOTE: self.currentMatchList is no longer a dictionary, and no longerhas
        #       a "totalGames" field. 
        # self.currentMatchList = {'totalGames': 9999}
        # self.matchListLength = 9999;
        if (matches == []):
            self.matchListLength = len(self.matchIds);
            self.i = len(self.matchIds);
            return;

        self.currentMatchList = matches # ['totalGames']
        self.i += 100

#Helper function: separates the "participantStats", returning information for
# both teams ("team100", "team200") along with the "gameWide" stats. 
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
# We only update "rank" if the match was played within a week of the update time
# to preserve a fuzzy amount of accuracy.  
def rankForJsonLoader(self, gameCreation):
    secondsInFiveDays = 432000
    if time.time() - secondsInFiveDays < gameCreation:
        rank = self.summonerRank
    else:
        rank = None
    return rank
    #e.g.:
    #1612032984 - 432000

#Helper fuNCTION: currently WIP. 
# Will return a scoring of the summoner's performance in this game based 
# primarily on early game metrics (most relevant for the jungle role). 
def EPICGGSCORE(self):
    return None


#Helper function: Uses the timeline data of all of the summoners to tally up 
# basic game stats, like the number of kills, deaths, assists, etc. 
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
        #contents of minuteDictionary :
        # [ 'participantFrames (dict) ', 'events (list)', 'timestamp (milliseconds)']

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

#Leading function: Given a self.j index, attempts to access the v4Match and v4Timeline
# information. If both API calls are functional, then by relying on the upper
# helper functions, update "self.matchIds" with relevant match data. 

#NOTE: v4Match may be depreciated, so this does not work. 
#NOTE: to decrease the data space, it is WIP to decrease the amount of information
#       that is stored in "self.matchIds[self.j]"
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
        self.matchIds[self.j]['EPICGGSCORE'] = self.EPICGGSCORE() #NULL
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

#Helper: returns the participant ID (integer from 1-10) for the summoner. 
def getParticipantIdOfSummoner(self, participants):
    for participant in participants:
        if participant['player']['currentAccountId'] == self.app.summonerInfo['accountId']:
            return participant['participantId']

#TimerFired: 2 modes:
#Mode 1: updating: runs through the updateControllers.
#Mode 2: overview: manages the page in overview mode. 
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
    if self.i == 0:
        matchIdLoader(self)
        #time of the most recent match
        #NOTE: TIMESTAMPS NO LONGER EXIST ANYMORE! have to phase out "self.mostRecentMatchDate"
        self.mostRecentMatchDate = self.matchHistory[0]['timestamp']
        #NOTE: use "self.mostRecentMatchId"?
        #toggle variable.
        self.matchIdsPrepared = False
    elif self.i < self.matchListLength:
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
            fileName = self.app.summonerInfo['accountId']
            with open(fileName, 'w') as outfile:
                json.dump(self.matchHistory, outfile, indent=4)
            appStarted(self)

def updateController(self):
    #if no games are loaded, or if not all "game details" are loaded yet. 
    if self.i < self.matchListLength:
        matchIdLoader(self)
    elif self.i >= self.matchListLength:
        #Load the match information and then store it into a file and restarting this app mode.
        #printf("Number of matches: {len(self.matchIds)}")

        #if "self.j" hasn't iterated through the matchID list, continue with
        # the detailed updating process. 
        if self.j < len(self.matchIds):
            matchJsonLoader(self)

        #Else, store the information into the text file and restart summonerinfo
        else:
            self.updating = False
            fileName = self.app.summonerInfo['accountId']
            #file = self.summonerName.lower()
            #for i in range(len(file)):
            #    if file[i] == " ":
            #        file = file[:i] + file[i+1:]
            #fileName = file + 'Data.txt'
            with open(fileName, 'w') as outfile:
                json.dump(self.matchIds, outfile, indent=4)
            appStarted(self)




###############################################################################
#
# REDRAW ALL

def redrawAll(self, canvas):
    summoner_info_redrawall.redrawAll(self, canvas)