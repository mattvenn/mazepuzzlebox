import json
import simplejson as json
from SVG import *
import math
import sys
from django.conf import settings
#import mazepuzzlebox.createbox.models 

endX = 2
endY = 4
startX = 15
startY = 5
#endX = mazepuzzlebox.createbox.models.endX
#endY = mazepuzzlebox.createbox.models.endY
#startX = mazepuzzlebox.createbox.models.startX
#startY = mazepuzzlebox.createbox.models.startY
svgdir=settings.ROOT_DIR + "mazepuzzlebox/DXF/processSVG/"
passageWidth = 5
linePoints = []
maze = None
xCells = None
yCells = None
drawColor = None
dirs = [ "LEFT", "RIGHT", "TOP", "BOTTOM" ]

#cell utility class
class Cell():

    def __init__(self,x,y,passage):
        self.x = x
        self.y = y
        self.passage = passage

    def is_passage(self):
        return self.passage

    def is_neighbour_passage(self,dir):
        if dir == "LEFT": 
             if self.x > 0:
                if maze[self.x-1][self.y].is_passage():
                    return True
        if dir == "RIGHT": 
             if self.x < xCells - 1:
                if maze[self.x+1][self.y].is_passage():
                    return True
        if dir == "TOP": 
             if self.y > 0:
                if maze[self.x][self.y-1].is_passage():
                    return True
        if dir == "BOTTOM": 
             if self.y < yCells -1:
                if maze[self.x][self.y+1].is_passage():
                    return True
        return False

#functions for drawing
def endShape():
    global drawColor,linePoints
    #import pdb; pdb.set_trace()
    d.idLine('mline',points=linePoints) 
    linePoints = []

def drawStartAndEnd():
    w = passageWidth
    #start cross
    vertex(startX*w,startY*w)
    vertex(startX*w+w,startY*w+w)
    endShape()
    vertex(startX*w+w,startY*w)
    vertex(startX*w,startY*w+w)
    endShape()

    #end circle
    rad = w/2
    #what the hell is this about?! #SVGBUST
    rad *= 1.25
    d.idCircle('line',(endX*w+rad+transX,endY*w+rad+transY),rad)

def drawMazeOutline(x,y):
    w = passageWidth
    s = w / 2
    vertex(0-s,0-s)
    vertex(x*w+s,0-s)
    endShape()
    vertex(x*w+s,0-s)
    vertex(x*w+s,y*w+s)
    endShape()
    vertex(x*w+s,y*w+s)
    vertex(0-s,y*w+s)
    endShape()
    vertex(0-s,y*w+s)
    vertex(0-s,0-s)
    endShape()


def vertex(x,y):
    #mirror
#    y = 0 - y
    #rotate; thanks http://en.wikipedia.org/wiki/Rotation_matrix#Basic_rotations
#    angle = 3 * (math.pi / 2 )
#    rotX = x * math.cos(angle) - y * math.sin(angle)
#    rotY = x * math.sin(angle) + y * math.cos(angle)
#    x = rotX
#    y = rotY
    #translate
    global transX, transY
    x = x+transX
    y = y+transY
    linePoints.append([x,y])

def drawLines(x,y, dir, lineStarted):
    if maze[x][y].passage and not maze[x][y].is_neighbour_passage(dir):
        if not lineStarted:
            #beginShape()
            lineStarted = True
            drawVertex(dir,x,y)
    else:
        drawVertex(dir,x,y)
        endShape()
        lineStarted = False

    return lineStarted

def drawVertex( dir, x,y ):
    if dir == "LEFT" : 
        vertex(x*passageWidth,y*passageWidth)
    if dir == "RIGHT" :
        vertex(x*passageWidth+passageWidth,y*passageWidth)
    if dir == "TOP":
        vertex(x*passageWidth,y*passageWidth)
    if dir == "BOTTOM":
        vertex(x*passageWidth,y*passageWidth+passageWidth)

def drawDXFMaze():
    global linePoints
    lineStarted = False
    linePoints = []
    for dir in range(2):
        for x in range(xCells):
            for y in range(yCells):
                lineStarted = drawLines(x,y,dirs[dir],lineStarted);

            if lineStarted:
                lineStarted = False
                drawVertex(dirs[dir],x,yCells)
                endShape()

    # top and bottom lines are missing when we hit the wall on the right
    for dir in range(2,4):
        for y in range(yCells):
            for x in range(xCells):
                lineStarted = drawLines(x,y,dirs[dir],lineStarted)

            if lineStarted:
                lineStarted = False
                drawVertex(dirs[dir],xCells,y)
                endShape()



##main start
#prep drawing
def drawMaze( jstr,box ):
    global transX,transY,d,drawColor,maze,xCells,yCells
    (xCells,yCells)=box.getDimensions()
    d=Drawing(svgdir+'instructionsmaze.svg')

    #import the maze
    matrix = json.loads( jstr )
    maze = [[Cell(x,y,matrix[x][y]) for y in range(yCells)] for x in range(xCells)]

    #what are these units?!
    #SVGBUST
    transX = 10
    transY = 102 #190
    drawDXFMaze()
    drawStartAndEnd()
    drawMazeOutline(xCells,yCells)
    d.saveas()
