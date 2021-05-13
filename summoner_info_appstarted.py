import requests
import json



#this should be placed inside of a dictionary. 'unranked', 'bronze', .... 'challenger'
def loadRanks(self):
    self.rankIcons = dict()
    temp = self.loadImage('images/Emblem_Iron.png')
    self.rankIcons['iron'] = self.scaleImage(temp, 1/6)
    temp = self.loadImage('images/Emblem_Bronze.png')
    self.rankIcons['bronze'] = self.scaleImage(temp, 1/6)
    temp = self.loadImage('images/Emblem_Silver.png')
    self.rankIcons['silver'] = self.scaleImage(temp, 1/6)
    temp = self.loadImage('images/Emblem_Gold.png')
    self.rankIcons['gold'] = self.scaleImage(temp, 1/6)
    temp = self.loadImage('images/Emblem_Platinum.png')
    self.rankIcons['platinum'] = self.scaleImage(temp, 1/6)
    temp = self.loadImage('images/Emblem_Diamond.png')
    self.rankIcons['diamond'] = self.scaleImage(temp, 1/6)
    temp = self.loadImage('images/Emblem_Master.png')
    self.rankIcons['master'] = self.scaleImage(temp, 1/6)
    temp = self.loadImage('images/Emblem_Grandmaster.png')
    self.rankIcons['grandmaster'] = self.scaleImage(temp, 1/6)
    temp = self.loadImage('images/Emblem_Challenger.png')
    self.rankIcons['challenger'] = self.scaleImage(temp, 1/6)

    self.rankIcons['unranked'] = self.rankIcons['challenger']



#loads the summoner icons into self.summonerSpellIcons.
#This could fail in the future, but removes need to use internet to slowly load these images in. 
def loadSummonerSpells(self):
    self.summonerSpellIcons = dict()
    names = {'21': 'SummonerBarrier.png', '1': 'SummonerBoost.png', '14': 'SummonerDot.png', 
    '3': 'SummonerExhaust.png', '4': 'SummonerFlash.png', '6': 'SummonerHaste.png', 
    '7': 'SummonerHeal.png', '13': 'SummonerMana.png', '30': 'SummonerPoroRecall.png', 
    '31': 'SummonerPoroThrow.png', '11': 'SummonerSmite.png', '39': 'SummonerSnowURFSnowball_Mark.png', 
    '32': 'SummonerSnowball.png', '12': 'SummonerTeleport.png', '0': 'placeholder.png'} 

    for idNum in names:
        tempImg = self.loadImage('images/' + names[idNum])
        self.summonerSpellIcons[idNum] = self.scaleImage(tempImg, 1/2)
    #print(self.summonerSpellIcons)


def loadChampionDetails(self):
    versions = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
    latestVersion = versions.json()[0]
    championLinks = 'http://ddragon.leagueoflegends.com/cdn/' + latestVersion + '/data/en_US/champion.json'
    championData = requests.get(championLinks)
    championToID = championData.json()['data']
    self.IDtoChampion = dict()
    for championName in championToID:
        self.IDtoChampion[championToID[championName]['key']] = championName
    self.championToID = championToID
    self.latestVersion = latestVersion
    self.app.champIdToName = self.IDtoChampion



def loadQueueDetails(self):
    gameModes = requests.get('http://static.developer.riotgames.com/docs/lol/queues.json')
    #if gameModes.status_code == 200
    gameModes = gameModes.json()
    self.queueToDescription = dict()
    for dictionary in gameModes:
        description = dictionary['description']
        if description == None:
            description = "Custom games"
        index = description.find(' games')
        if index >= 0:
            description = description[:index]
        index = description.find('5v5 ')
        if index >= 0:
            description = description[index+4:]
        self.queueToDescription[dictionary['queueId']] = description
    #print(self.queueToDescription)


#
##
#
#
# 2.

def summonerIconRank(self):
    #loading in summoner Icon
    url = "https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon" + str(self.app.summonerInfo['profileIconId']) + ".png"
    self.summonerIcon = self.loadImage(url)
    self.summonerName = self.app.summonerInfo['name']
    self.summonerLevel = self.app.summonerInfo['summonerLevel']
    #Rank information
    if self.app.summonerInfo['tier'] == None:
        self.summonerRank = "Unranked"
        self.summonerTier = "unranked"
    else:
        self.summonerRank = self.app.summonerInfo['tier'].title() + " " +self.app.summonerInfo['rank']
        self.summonerTier = self.app.summonerInfo['tier'].lower()



def preexistingMatchHistoryInformation(self):
    #Preexisting match history information
    file = self.summonerName.lower()
    for i in range(len(file)):
        if file[i] == " ":
            file = file[:i] + file[i+1:]
    fileName = file + 'Data.txt'
    try:
        with open(fileName) as json_file:
            self.matchHistory = json.load(json_file)
    except:
        self.matchHistory = None
        print("Existing match history not found!")


#gets the kda, number of wins, number losses, total games?
def recentFifteenGames(self):
    championsPlayed = dict()
    if self.matchHistory == None:
        print('Unable to obtain recentFifteenGames')
        self.fifteenStats = None
        return
    
    for i in range(20):
        try:
            match = self.matchHistory[i]
        except:
            print("skipp")
            continue #continue when there are less than 20/15 matches being played
        
        championPlayedKey = match['champion']
        championPlayed = self.IDtoChampion[str(championPlayedKey)]
        #championsPlayed[championPlayed] = championsPlayed.get(championPlayed, 0) + 1
        championInfo = championsPlayed.get(championPlayed, None)
        if championInfo == None:
            championInfo = dict()
            championInfo['games'] = 0
            championInfo['wins'] = 0
            championInfo['losses'] = 0
            championInfo['kills'] = 0
            championInfo['deaths'] = 0
            championInfo['assists'] = 0
        
        championInfo['kills'] += match['summonerStats']['stats']['kills']
        championInfo['deaths'] += match['summonerStats']['stats']['deaths']
        championInfo['assists'] += match['summonerStats']['stats']['assists']

        championInfo['games'] += 1
        if match['summonerStats']['stats']['win']:
            championInfo['wins'] += 1
        else:
            championInfo['losses'] += 1
        championsPlayed[championPlayed] = championInfo

    
    result = (self.sortDictionary(championsPlayed, 'games'))
    result.reverse()
    self.fifteenStats = result[:3]
    
    for dictionary in self.fifteenStats:
        for key in dictionary:
            tempKey = key
        url = 'https://raw.communitydragon.org/latest/game/assets/characters/' + tempKey.lower() + '/hud/' + tempKey.lower() + '_circle.png'
        url2 = 'https://raw.communitydragon.org/latest/game/assets/characters/' + tempKey.lower() + '/hud/' + tempKey.lower() + '_circle_0.png'
        url3 = 'https://raw.communitydragon.org/latest/game/assets/characters/' + tempKey.lower() + '/hud/' + tempKey.lower() + '_circle_1.png'
        print(url2)
        print()
        try:
            tmep = self.loadImage(url)
            dictionary[tempKey]['icon'] = self.scaleImage(tmep, 1/2)
            print(tmep.size)
        except:
            try:
                tmep = self.loadImage(url2)
                dictionary[tempKey]['icon'] = self.scaleImage(tmep, 1/2)
            except:
                tmep = self.loadImage(url3)
                dictionary[tempKey]['icon'] = self.scaleImage(tmep, 1/2)
    print(self.fifteenStats)



def loadAggregateStats(self):
    if self.matchHistory == None:
        self.aggregateGameStats = None
        self.rankedStats = None
        return
    self.aggregateGameStats = dict()
    self.rankedStats = {'games':0, 'wins':0, 'losses':0}
    for match in self.matchHistory:
        #match['timestamp'] is milliseconds epoch time, seasonStart is seconds
        if match['queue'] == 420 and match['timestamp']//1000 >= self.app.seasonStart: 
            self.rankedStats['games'] += 1
            if match['summonerStats']['stats']['win']:
                self.rankedStats['wins'] += 1
            else:
                self.rankedStats['losses'] += 1
        championPlayedKey = match['champion']
        championPlayed = self.IDtoChampion[str(championPlayedKey)]
        #champsPlayed[championPlayed] = champsPlayed.get(championPlayed, 0) + 1
        information = self.aggregateGameStats.get(championPlayed, None)

        #not necessarily effective, but it's "neater"
        if information == None: 
            information = dict()
            information['gamesPlayed'] = 0
            information['wins'] = 0
            information['losses'] = 0
            #stats
            information['totalDamage'] = 0
            information['totalTaken'] = 0
            information['visionScore'] = 0
            information['goldEarned'] = 0
            information['totalMinionsKilled'] = 0
            #KDA
            information['totalKills'] = 0
            information['totalDeaths'] = 0
            information['totalAssists'] = 0
            #game
            information['gameDuration'] = 0
            information['rankedMatches'] = 0

        if match['queue'] == 420:
            information['rankedMatches'] += 1
        if match['summonerStats']['stats']['win']:
            information['wins'] += 1
        else:
            information['losses'] += 1
        information['gamesPlayed'] += 1

        information['totalDamage'] += match['summonerStats']['stats']['totalDamageDealtToChampions']
        information['totalTaken'] += match['summonerStats']['stats']['totalDamageTaken']
        information['visionScore'] += match['summonerStats']['stats']['visionScore']
        information['goldEarned'] += match['summonerStats']['stats']['goldEarned']
        information['totalMinionsKilled'] += match['summonerStats']['stats']['totalMinionsKilled'] + match['summonerStats']['stats']['neutralMinionsKilled']
        information['totalKills'] += match['summonerStats']['stats']['kills']
        information['totalDeaths'] += match['summonerStats']['stats']['deaths']
        information['totalAssists'] += match['summonerStats']['stats']['assists']
        information['gameDuration'] += match['gameDuration']


        self.aggregateGameStats[championPlayed] = information
    #print(self.aggregateGameStats) #dictionary form
    #print(sortDictionary(self, self.aggregateGameStats, 'gamesPlayed')) #list form. 

    self.championStats = dict()
    for key in self.aggregateGameStats:
        temp = dict()
        numGames = self.aggregateGameStats[key]['gamesPlayed']
        temp['Games'] = numGames
        temp['Wins'] = self.aggregateGameStats[key]['wins']
        temp['Losses'] = self.aggregateGameStats[key]['losses']
        temp['Win Rate'] = round(round(temp['Wins']/numGames, 3) * 100, 1)
        temp['Kills'] = round(self.aggregateGameStats[key]['totalKills']/numGames, 1)
        temp['Deaths'] = round(self.aggregateGameStats[key]['totalDeaths']/numGames, 1)
        temp['Assists'] = round(self.aggregateGameStats[key]['totalAssists']/numGames, 1)
        temp['Damage'] = round(self.aggregateGameStats[key]['totalDamage']/numGames, 1)
        temp['Dmg Taken'] = round(self.aggregateGameStats[key]['totalTaken']/numGames, 1)
        temp['Vision'] = round(self.aggregateGameStats[key]['visionScore']/numGames, 1)
        temp['Gold'] = round(self.aggregateGameStats[key]['goldEarned']/numGames, 1)
        temp['CS'] = round(self.aggregateGameStats[key]['totalMinionsKilled']/numGames, 1)
        temp['gameDuration'] = round(self.aggregateGameStats[key]['gameDuration']/numGames)
        self.championStats[key] = temp
    #print(self.championStats)

    self.sortedAggregateStats = sortDictionary(self, self.championStats, self.sortingFactor)
    self.sortedAggregateStats.reverse()
    #print(self.sortedAggregateStats)
    #buttons:
    #['Games', 'Wins', 'Losses', 'Win Rate', 'Kills', 'Deaths', 'Assists', 'Damage', 'Dmg Taken', 'Vision', 'Gold', 'CS']

def create_buttons(self):
    #creating the buttons
    self.buttons = []
    x = Button.xsize/2 + self.pageLeft
    y = 350
    self.buttons.append(Button(x, y, 'Champion'))
    traits = ['Games', 'Wins', 'Losses', 'Win Rate', 'Kills', 'Deaths', 'Assists', 'Damage', 'Dmg Taken', 'Vision', 'Gold', 'CS']
    for i in range(len(traits)):
        self.buttons.append(Button(x+Button.xsize*(1+i),y, traits[i]))



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

def swap(a, i, j):
    (a[i], a[j]) = (a[j], a[i])