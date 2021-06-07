#summoner gui.
#uses a modal app design,
#has data collection algorithms, sorting algorithms, and a advanced gui. 

from cmu_112_graphics import *
import json
import time
import requests

import search_screen
import modal_app_init
import summoner_info




# Initializes some variables for the app. 
# Initializes the API. 
class MyModalApp(ModalApp):
    def appStarted(app):
        app.searchScreenMode = SearchScreen()
        app.summonerInfoMode = SummonerInfo()
        app.matchInfoMode = MatchInfo()
        modal_app_init.appStarted(app);


class MatchInfo(Mode):
    def appStarted(self):
        #drawing stuff
        self.pageLeft = 220
        self.currMatch = 0
        MatchInfo.loadImages(self)
        MatchInfo.loadPerformanceIndicators(self)
        MatchInfo.loadTeamStatistics(self)
    
    def loadImages(self):
        pass

    def loadPerformanceIndicators(self):
        #print("most games are determined at about 15 minutes. Optimized early games are important.")
        self.ten = None
        self.fourteen = None

        if len(self.app.matchInfo['summonerIdTimeline']) >= 10:
            timeline = self.app.matchInfo['summonerIdTimeline'][10]
            min = 10
            gold = timeline['frame']['totalGold']
            level = timeline['frame']['level']
            cs = timeline['frame']["minionsKilled"] + timeline['frame']["jungleMinionsKilled"]
            ka = timeline['frame']['kills'] + timeline['frame']['assists']
            d = timeline['frame']['deaths']
            dragons = timeline['frame']['dragons']
            heralds = timeline['frame']['heralds']
            towers = timeline['frame']['towers']
            t1 = f"At {min} minutes:"
            t2 = f"{level} level with {round(cs/min, 1)} cs/min."
            t3 = f"{ka} kills and assists, {d} deaths"
            t4 = f"{dragons} dragons, {heralds} herald, and {towers} towers taken. "
            t5 = f"Economy: {gold} gold. "
            self.ten = [t1, t2, t3, t4, t5]

        if len(self.app.matchInfo['summonerIdTimeline']) >= 14:
            timeline = self.app.matchInfo['summonerIdTimeline'][14]
            min = 14
            tentimeline = self.app.matchInfo['summonerIdTimeline'][10]
            csss = timeline['frame']["minionsKilled"] + timeline['frame']["jungleMinionsKilled"] - (tentimeline['frame']["minionsKilled"] + tentimeline['frame']["jungleMinionsKilled"])
            gold = timeline['frame']['totalGold']
            level = timeline['frame']['level']
            cs = timeline['frame']["minionsKilled"] + timeline['frame']["jungleMinionsKilled"]
            ka = timeline['frame']['kills'] + timeline['frame']['assists']
            d = timeline['frame']['deaths']
            dragons = timeline['frame']['dragons']
            heralds = timeline['frame']['heralds']
            towers = timeline['frame']['towers']
            t1 = f"At {min} minutes:"
            t2 = f"{level} level with {round(csss/4, 1)} cs/min between 10-14 min."
            t3 = f"{ka} kills and assists, {d} deaths"
            t4 = f"{dragons} dragons, {heralds} herald, and {towers} towers taken. "
            t5 = f"Economy: {gold} gold. "
            self.fourteen = [t1, t2, t3, t4, t5]

    def loadTeamStatistics(self):
        matchInfo = self.app.matchInfo #decrease variable name length

        team100Stats = matchInfo['team100']['players']
        team200Stats = matchInfo['team200']['players']
        #Team 1:
        self.team1 = []
        self.team2 = []
        for player in team100Stats:
            playerStats = dict()

            partId = player['participantId']
            summonerNameCollection = matchInfo['participantIdentities']
            playerStats['summonerName'] = MatchInfo.summonerName(self, partId, summonerNameCollection)

            playerStats['champion'] = self.app.champIdToName[str(player["championId"])]
            kda = f"{player['stats']['kills']}/{player['stats']['deaths']}/{player['stats']['assists']}  ({round((player['stats']['kills']+player['stats']['assists'])/(player['stats']['deaths']), 2)})"
            playerStats['kda'] = kda
            kills = matchInfo['team100']['kills']
            kp = f"{round(((player['stats']['kills']+player['stats']['assists'])/kills)*100, 2)}%"
            playerStats['dmgDealt'] = player['stats']['totalDamageDealtToChampions']
            #playerStats['dmgTaken'] = player['stats']['totalDamageTaken']
            playerStats['killParticipation'] = kp
            playerStats['visionScore'] = player['stats']['visionScore']
            playerStats['creepScore'] = player['stats']['totalMinionsKilled'] + player['stats']['neutralMinionsKilled']
            playerStats['gold'] = player['stats']['goldEarned']
            self.team1.append(playerStats)
        self.team1win = player['stats']['win']
        #team 2
        for player in team200Stats:
            playerStats = dict()
            partId = player['participantId']
            summonerNameCollection = matchInfo['participantIdentities']
            playerStats['summonerName'] = MatchInfo.summonerName(self, partId, summonerNameCollection)
            playerStats['champion'] = self.app.champIdToName[str(player["championId"])]
            kda = f"{player['stats']['kills']}/{player['stats']['deaths']}/{player['stats']['assists']}  ({round((player['stats']['kills']+player['stats']['assists'])/(player['stats']['deaths']), 2)})"
            playerStats['kda'] = kda
            kills = matchInfo['team200']['kills']
            kp = f"{round(((player['stats']['kills']+player['stats']['assists'])/kills)*100, 2)}%"
            playerStats['dmgDealt'] = player['stats']['totalDamageDealtToChampions']
            #playerStats['dmgTaken'] = player['stats']['totalDamageTaken']
            playerStats['killParticipation'] = kp
            playerStats['visionScore'] = player['stats']['visionScore']
            playerStats['creepScore'] = player['stats']['totalMinionsKilled'] + player['stats']['neutralMinionsKilled']
            playerStats['gold'] = player['stats']['goldEarned']
            self.team2.append(playerStats)
        self.team2win = player['stats']['win']
        #print(self.team1)
        #print(self.team2)
        self.teamStatisticsTitle = ["Summoner", "Champion", "KDA", "Dmg Dealt", "KP", "Vision", "CS", "Gold"]



    def summonerName(self, partId, summonerNameCollection):
        for summoner in summonerNameCollection:
            if summoner['participantId'] == partId:
                return summoner['player']['summonerName']
        return summonerNameCollection[0]['player']['summonerName'] #shouldn't ever get here. 

    def keyPressed(self, event):
        if event.key == "Escape":
            self.app.setActiveMode(self.app.summonerInfoMode)
        else:
            MatchInfo.loadTeamStatistics(self)
    
    def timerFired(self):
        if self.app.currMatch != self.currMatch:
            MatchInfo.loadPerformanceIndicators(self)
            MatchInfo.loadTeamStatistics(self)

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/2, text=':(')
        #create the background
        canvas.create_rectangle(self.pageLeft-20, 0, self.width-self.pageLeft+20, self.height, fill='light blue', width = 0)


        #performance
        canvas.create_rectangle(self.pageLeft, self.height*(2/3), self.width-self.pageLeft, self.height-20)
        canvas.create_text(self.pageLeft+10, self.height*(2/3)+10, anchor='nw', text="Performance Indicators")
        
        if self.ten != None:
            pageLeft = self.pageLeft+10
            initHeight = self.height * (2/3) + 30
            heightAdjust = 25 #number of pixels between each line. 
            for i in range(len(self.ten)):
                canvas.create_text(pageLeft, initHeight + heightAdjust*i, anchor = 'nw', text=self.ten[i])
        
        if self.fourteen != None:
            pageLeft = self.pageLeft+250
            initHeight = self.height * (2/3) + 30
            heightAdjust = 25 #number of pixels between each line. 
            for i in range(len(self.fourteen)):
                canvas.create_text(pageLeft, initHeight + heightAdjust*i, anchor = 'nw', text=self.fourteen[i])
        MatchInfo.drawTeam1(self, canvas)
        MatchInfo.drawTeam2(self, canvas)
        """
        EPICGGSCORE in the perspective of Nunu *(and at 14 minutes)
        CS/min: needs to be above ~6 to have a good econ.
        Exp: need to be at level 9 to be on pace with the others in the game
        KA: can depend on the number of deaths, aim for at least 3
        d: having 2 or more deaths can often spell doom for the game, even with high KA. 
            understand why you are dying if your deaths are higher than 1. 
        drag/herald: definitely try to have 1 of these secured. maybe not the best 
            thing to measure, but having 3 of these is perfect control, which 
            indicates that the team as a whole is snowballing really hard. If you lose
            despite having 2+ dragons, that is a really bad sign.
            If you lose but have <=1, that can be attributed to many different reasons (probably)
        towers: Towers are definitely a pretty strong sign, but they are pretty rare to get down 
            at 14 minutes. 
            if you lose despite taking down 2+ towers at 14, that is a terrible sign.
        """

    def drawTeam1(self, canvas):
        if self.team1win:
            color = "green"
        else:
            color = "red"
        w = 330
        h = 150
        hmargin = 35
        wmargin = 90
        canvas.create_rectangle(w-50, h-60, w+wmargin*8-50, h+hmargin*5, fill=color, width = 0)
        for i in range(len(self.teamStatisticsTitle)):
            name = self.teamStatisticsTitle[i]
            canvas.create_text(w + wmargin*i, h-40, text = name, font = "arial 11 bold")
        for i in range(len(self.team1)):
            player = self.team1[i]
            height = h + hmargin*i
            k = 0
            for keyCat in player:
                tempVar = player[keyCat]
                width = w + wmargin*k
                canvas.create_text(width, height, text=tempVar)
                k = k + 1

    def drawTeam2(self, canvas):
        if self.team2win:
            color = "green"
        else:
            color = "red"
        w = 330
        h = 400
        hmargin = 35
        wmargin = 90
        canvas.create_rectangle(w-50, h-60, w+wmargin*8-50, h+hmargin*5, fill=color, width = 0)
        for i in range(len(self.teamStatisticsTitle)):
            name = self.teamStatisticsTitle[i]
            canvas.create_text(w + wmargin*i, h-40, text = name, font = "arial 11 bold")

        for i in range(len(self.team2)):
            player = self.team2[i]
            height = h + hmargin*i
            k = 0
            for keyCat in player:
                tempVar = player[keyCat]
                width = w + wmargin*k
                canvas.create_text(width, height, text=tempVar)
                k = k + 1

class SummonerInfo(Mode):
    def appStarted(self):
        summoner_info.appStarted(self)

    def mousePressed(self, event):
        summoner_info.mousePressed(self, event);


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
            participantIdOfSummoner = SummonerInfo.getParticipantIdOfSummoner(self, participants)
            participantStats = v4Match['participants']
            statsOfSummoner = None
            for participant in participantStats:
                if participant['participantId'] == participantIdOfSummoner:
                    statsOfSummoner = participant
            team100, team200, gameWide = SummonerInfo.team100team200Helper(self, participantStats)
            rank = SummonerInfo.rankForJsonLoader(self, v4Match['gameCreation']//1000)
            timeline, skillOrder = SummonerInfo.summonerIdTimeline(self, participantIdOfSummoner, v4Timeline)
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
            SummonerInfo.updateController(self)
        elif self.updating and self.preexisting:
            SummonerInfo.updatePreexistingController(self)
        
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
            SummonerInfo.matchIdLoader(self)
            #time of the most recent match
            self.mostRecentMatchDate = self.matchHistory[0]['timestamp']
            #toggle variable.
            self.matchIdsPrepared = False
        elif self.i < self.currentMatchList['totalGames']:
            SummonerInfo.matchIdLoader(self)
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
                SummonerInfo.matchJsonLoader(self)
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
                SummonerInfo.appStarted(self)

    def updateController(self):
        if self.currentMatchList == None:
            SummonerInfo.matchIdLoader(self)
        elif self.i < self.currentMatchList['totalGames']:
            SummonerInfo.matchIdLoader(self)
        elif self.i >= self.currentMatchList['totalGames']:
            #need to start loading the match information, eventually storing it into a json file and restarting this app mode.
            #print(f"Number of matches: {len(self.matchIds)}")
            if self.j < len(self.matchIds):
                SummonerInfo.matchJsonLoader(self)
            else:
                self.updating = False
                file = self.summonerName.lower()
                for i in range(len(file)):
                    if file[i] == " ":
                        file = file[:i] + file[i+1:]
                fileName = file + 'Data.txt'
                with open(fileName, 'w') as outfile:
                    json.dump(self.matchIds, outfile, indent=4)
                SummonerInfo.appStarted(self)

    def redrawAll(self, canvas):
        #Header:
        pageLeft = self.pageLeft #120???
        #page color:
        canvas.create_rectangle(pageLeft-20, 0, self.width-pageLeft+20, self.height, fill = "light blue", width = 0)

        #draw the mode:
        if self.mode == "overview":
            SummonerInfo.drawOverview(self, canvas)
        elif self.mode == "champions":
            SummonerInfo.drawChampions(self, canvas)
        elif self.mode == "improvement":
            SummonerInfo.drawImprovement(self, canvas)

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
                color = SummonerInfo.rgbString(97, 194, 75) #random green
                victoryText = "Win"
            else:
                color = SummonerInfo.rgbString(226, 182, 179) #soft red
                victoryText  = "Loss"
            x0 = self.pageLeft
            y0 = startY + (size)*i+buffer
            x1 = self.width-self.pageLeft
            y1 = startY + (size) * (i+1)
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            
            #queue !
            queue = self.queueToDescription[(matchDetails['queue'])]
            canvas.create_text(x0+40, y0 + size*(1/10), text=queue, font='calibri 10')

            min, sec = SummonerInfo.secondsToMinutes(matchDetails['gameDuration'])
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


    def create_buttons(self):
        #creating the buttons
        self.buttons = []
        x = Button.xsize/2 + self.pageLeft
        y = 350
        self.buttons.append(Button(x, y, 'Champion'))
        traits = ['Games', 'Wins', 'Losses', 'Win Rate', 'Kills', 'Deaths', 'Assists', 'Damage', 'Dmg Taken', 'Vision', 'Gold', 'CS']
        for i in range(len(traits)):
            self.buttons.append(Button(x+Button.xsize*(1+i),y, traits[i]))

    def drawImprovement(self, canvas):
        start = 350
        size = 120
        canvas.create_rectangle(self.pageLeft, start, self.width-self.pageLeft, start + size)
        canvas.create_text(self.width/2, start + size/2, text='work in progress')

    #code from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    def rgbString(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'



# Initial screen that comes up when the app is open: 
class SearchScreen(Mode):
    def appStarted(self):
        search_screen.appStarted(self)

    def keyPressed(self, event):
        search_screen.keyPressed(self, event)

    def timerFired(self):
        search_screen.timerFired(self)

    def redrawAll(self, canvas):
        search_screen.redrawAll(self, canvas)



app = MyModalApp(width=1280, height=1000)