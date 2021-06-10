from cmu_112_graphics import *
import time


#Header:
def redrawAll(self, canvas):
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
            kd = f"KDA: {round(k+a, 2)}:1" # 2 decimal places
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

