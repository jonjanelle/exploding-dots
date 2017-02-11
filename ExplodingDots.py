'''
Demonstration of a simple game
based on James Tanton's "Exploding Dots"
model for understanding place value, number base, and 
arithmetic operations.

This version only demonstrates addition in an arbitrary base.
Bases are limited to 1-12 (mainly to facilitate the drawing of actual dots on the models)

Puzzle types include:
1) Starting and ending states for the machine are given, machine type known (i.e. 1 <- 3), 
   player must determine what was combined with starting state to yield ending state

2) Starting state and added blocks given, machine type know, player needs to determine ending state

3) Machine type is unknown (but of form 1 <- ?), two examples of correct puzzles given,
   user needs to determine machine type before performing one of the above

4) Machine type is of form y <- x, where x != y, x and y positive integers.


To Do:
 - Make a cell class so that cell rects, borders, and dot counts
   are handled internally within one object

'''
import pygame, sys
from FillGradient import fill_gradient
pygame.init()

#Define some color constants
####################
Color = {"white":(255,255,255), "black":(0,0,0),"red":(255,0,0),
         "green":(0,255,0),"blue":(0,0,255),"yellow":(255,255,0),
         "purple":(128,0,128),"gray":(128,128,128)}


#Define window size constants
###################
sWIDTH = 800
sHEIGHT = 600


#Set machine type and label position
####################
machineType = (1,8) 

#Setup font
font = pygame.font.SysFont("bromine", 40)
machineLabelText = font.render(str(machineType[0])+u'\u2190'+str(machineType[1]), True, (50, 0, 200))
machineLabelPos = (sWIDTH-int(1.8 *machineLabelText.get_width()),sHEIGHT//20)
titleRect = pygame.Rect(machineLabelPos[0],machineLabelPos[1],machineLabelText.get_width(),machineLabelText.get_height())


#########################
#Begin program functions
#########################

def getBoxPoints(x,y,width,height):
    '''
    Get the list of tuples for the vertices of a rectangle with upper left corner
    at (x, y) and specified width and height
    '''
    return [(x,y),(x+width,y),(x+width,y+height),(x,y+height),(x,y)]


def drawCells(surface, n, x, y, width, height):
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
    if int(sWIDTH/n) < 1.1*width:
        width = int(sWIDTH/n*.8)
    
    cellRects = list()    
    for i in range(0,n):
        cellRects.append(pygame.Rect(x+width*i,y,width,height))
        pygame.draw.rect(surface,Color["gray"],cellRects[i],0)
        points = getBoxPoints(x+width*i,y,width,height)
        pygame.draw.lines(surface,Color["black"],False,points,2)
        
    return cellRects

def mouseInEditableCell(event,cellRects):
    '''
    Returns true if the pointer is currently within an editable cell, false otherwise
    '''
    for i in range(0, len(cellRects)):
        if cellRects[i].collidepoint(event.pos):
            return True
    return False


def getCellClicked(event,cellRects):
    '''
    returns the index in a rect array that corresponds
    to the editable cell clicked. Returns -1 if no cell clicked
    '''

    for i in range(0, len(cellRects)):
        if cellRects[i].collidepoint(event.pos):
            return i 
    return -1
    
def processLeftClick(event,cellRects,dotCounts):
    '''
    Add a dot to the cell clicked
    cellRects: Rects for editable cells
    
    Current goal: Just draw one big red dot in the middle
    '''
    cellIdx = getCellClicked(event,cellRects)
    if cellIdx >= 0: #Editable cell left clicked, need to add a dot
        dotCounts[cellIdx]+=1
        explodeLeft(dotCounts)
    elif titleRect.collidepoint(event.pos):
        global machineType,machineLabelText
        if machineType[1] < 16:
            machineType = (machineType[0],machineType[1]+1)
            machineLabelText = font.render(str(machineType[0])+u'\u2190'+str(machineType[1]), True, (50, 0, 200))

def processRightClick(event,cellRects,dotCounts):
    '''
    Remove a dot from the cell clicked
    '''
    cellIdx = getCellClicked(event,cellRects)
    if cellIdx >= 0: #Editable cell left clicked, need to add a dot
        dotCounts[cellIdx]-=1   

    elif titleRect.collidepoint(event.pos):
        global machineType,machineLabelText
        if machineType[1]>2:
            machineType = (machineType[0],machineType[1]-1)
            machineLabelText = font.render(str(machineType[0])+u'\u2190'+str(machineType[1]), True, (50, 0, 200))

def getBoardValue(dotCounts):
    '''
    Calculate the numerical value of the current dot configuration and machine type
    '''
    cellCnt = len(dotCounts)
    val = 0
    for i in range(cellCnt):
        val += dotCounts[i]*(machineType[1]**(cellCnt-i-1))
    return val

def drawCellDots(surface,cellRects,dotCounts):
    '''
    Draw dots within cells that indicate value
    '''
    for i in range(len(cellRects)):
        if dotCounts[i] != 0:
            for j in range(abs(dotCounts[i])):
                x1 = int(cellRects[i].left + cellRects[i].width*(.2 + .2*(j%4)))
                y1 = int(cellRects[i].top + cellRects[i].height*(.2+j//4*.2))
                if dotCounts[i]>0:
                    pygame.draw.circle(surface,Color["green"],(x1,y1),5)
                else:
                    pygame.draw.circle(surface,Color["red"],(x1,y1),5)
            

    
def explodeLeft(dotCounts):
    '''
    Update dot counts by collapsing lower place values to higher if appropriate
    '''
    global machineType
    limit = machineType[1] #assume it's a 1 <- ? machine
    for i in range(len(dotCounts)-1,-1,-1):
        while abs(dotCounts[i])>=limit and i > 0:
            if dotCounts[i] > 0:
                dotCounts[i] -= limit
                dotCounts[i-1]+=1
            else:
                dotCounts[i] += limit
                dotCounts[i-1] -= 1

def unexplodeRight():
    '''
    Unexplodes a dot in the current position to the right. The value of the array is preserved (no dots removed)
    Bind this action to middle click?
    '''
    pass

def getRandomStartDots():
    '''
    To generate a random puzzle
    '''
    pass



def drawButton(surface,x,y,style = 0):
    if style == 0:
        buttonRect = pygame.Rect(x,y,60,20)
        pygame.draw.rect(surface,Color["black"],buttonRect)
        fill_gradient(surface, Color["red"], Color["gray"], buttonRect, vertical = True, forward = True)
    else:
        return
    


def mainLoop(surface, bgImg, titleImg):
    '''
    Begin main animation loop, event checking
    '''
    global machineType
    #Set number of cells and the dimensions for each cell
    nCells = 7
    cellDim = (80, 80)
    startX = (sWIDTH-nCells*cellDim[0]*.9)//2
    startY = 120

    cellRects = drawCells(surface,nCells,startX,startY,cellDim[0],cellDim[1])
    dotCounts = [0 for x in range(len(cellRects))] #start with no dots in every cell
    boardVal = 0

    #Begin main program loop
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    processLeftClick(event,cellRects,dotCounts)
                elif event.button == 3:
                    processRightClick(event,cellRects,dotCounts)
                boardVal=getBoardValue(dotCounts)
        
        
        
        surface.blit(bgImg,(0,0))
        surface.blit(titleImg,(0,0))
        cellRects = drawCells(surface,nCells,startX,startY,cellDim[0],cellDim[1])        
        drawCellDots(surface,cellRects,dotCounts)
        surface.blit(machineLabelText, machineLabelPos)
        surface.blit(font.render("Value: "+str(boardVal),True,Color["black"]),(sWIDTH//2.5,sHEIGHT//2.5))
        
        #####################
        #Experiemental Stuff
        #
        #drawButton(surface, 300, 300, style=0)
        
        #
        #####################
        
        pygame.display.update()
        

def main():
    '''
    Init main surface, load images, and begin main loop
    '''
    pygame.display.set_caption("Exploding Dots Demo")
    surface = pygame.display.set_mode((sWIDTH,sHEIGHT))
    bgImg = pygame.image.load("bg5.png").convert()
    titleImg = pygame.image.load("title.jpg").convert()
    titleImg.set_colorkey(Color["white"])
   
    mainLoop(surface,bgImg,titleImg)       

if __name__ == "__main__":
    main()
    
    
'''
Notes about mouse detection

if event.type == pygame.MOUSEBUTTONDOWN:
    print event.button

event.button can equal several integer values:
1 - left click
2 - middle click
3 - right click
4 - scroll up
5 - scroll down

Instead of an event, you can get the current button state as well:
pygame.mouse.get_pressed()

This returns a tuple:
(leftclick, middleclick, rightclick)

Each one is a boolean integer representing button up/down.
'''