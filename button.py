class Button(object):
    xsize = 64
    ysize = 30
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
    
    def draw(self, app, canvas):
        #canvas.create_rectangle(self.x-Button.xsize/2, self.y-Button.ysize/2, self.x + Button.xsize/2, self.y+Button.ysize/2)
        if app.sortingFactor == self.text:
            canvas.create_rectangle(self.x-Button.xsize/2, self.y-Button.ysize/2, self.x + Button.xsize/2, self.y+Button.ysize/2, fill='grey', width = 0)
        canvas.create_text(self.x, self.y, text=self.text)
    
    def pointInButton(self, px, py):
        if (self.x-Button.xsize/2 <= px <= self.x + Button.xsize/2 and
            self.y-Button.ysize/2 <= py <= self.y + Button.ysize/2):
            return self.text
        return None