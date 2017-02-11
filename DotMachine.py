import pygame

class DotMachine:
  
    def getValue(self):
        '''
        Get the current numerical value of the dots on the board
        '''
        pass
    def explodeLeft(self):
        '''
        Update dot counts by collapsing lower place values to higher if appropriate
        '''
        global machineType
        limit = machineType[1] #assume it's a 1 <- ? machine
        for i in range(len(self.dotCounts)-1,-1,-1):
            while abs(self.dotCounts[i])>=limit and i > 0:
                if self.dotCounts[i] > 0:
                    self.dotCounts[i] -= limit
                    self.dotCounts[i-1]+=1
                else:
                    self.dotCounts[i] += limit
                    self.dotCounts[i-1] -= 1
    
    def unexplodeRight(self):
        '''
        Unexplodes a dot in the current position to the right. The value of the array is preserved (no dots removed)
        Bind this action to middle click?
        '''
        pass
    
    
    def getBoxPoints(self, x,y,width,height):
        '''
        Get the list of tuples for the vertices of a rectangle with upper left corner
        at (x, y) and specified width and height
        '''
        return [(x,y),(x+width,y),(x+width,y+height),(x,y+height),(x,y)]
    
    def drawCells(self,surface, n, x, y, width, height):
        '''
        Draw a row of cells to represent place-value positions. If the specified
        cell width and height would cause parts of cells to be drawn off screen,
        then automatic resizing occurs
        
        surface: A pygame surface on which to draw
        n: The number of cells to draw
        x,y: The coordinates of the upper-left corner of the grid
        width: The width of one cell in pixels
        height: The height of one cell in pixels
        
        Returns a list of pygame.Rect objects corresponding to each cell drawn 
        '''
        Color = {"white":(255,255,255), "black":(0,0,0),"red":(255,0,0),
         "green":(0,255,0),"blue":(0,0,255),"yellow":(255,255,0),
         "purple":(128,0,128),"gray":(128,128,128)}
        
        if int(self.sWIDTH/n) < 1.1*width:
            width = int(self.sWIDTH/n*.8)
        
        cellRects = list()    
        for i in range(0,n):
            cellRects.append(pygame.Rect(x+width*i,y,width,height))
            pygame.draw.rect(surface,Color["gray"],cellRects[i],0)
            points = self.getBoxPoints(x+width*i,y,width,height)
            pygame.draw.lines(surface,Color["black"],False,points,2)
            
        return cellRects
    
    def __init__(self):
        self.sWIDTH = 800
        self.sHEIGHT = 600
        self.nCells = 7
        self.cellDim = (80, 80)
        
        self.cellRects = self.drawCells(self.surface,self.nCells,self.startX,self.startY,self.cellDim[0],self.cellDim[1])
        self.dotCounts = [0 for x in range(len(self.cellRects))] #start with no dots in every cell
        self.boardVal = 0