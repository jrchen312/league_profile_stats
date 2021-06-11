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
        summoner_info.mousePressed(self, event)

    def keyPressed(self, event):
        summoner_info.keyPressed(self, event)
        if event.key == "Escape":
            MyModalApp.appStarted(self.app)
            #self.app.resetEverything = True
            #self.app.setActiveMode(app.searchScreenMode)

    def mouseDragged(self, event):
        summoner_info.mouseDragged(self, event)

    def timerFired(self):
        summoner_info.timerFired(self)

    def redrawAll(self, canvas):
        summoner_info.redrawAll(self, canvas)



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