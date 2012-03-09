import json
import simplejson as json
from SVG import *
import math
import sys
from django.conf import settings

dxfdir=settings.ROOT_DIR + "mazepuzzlebox/DXF/processDXF/"
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
    d.MLine(points=linePoints) 
    linePoints = []

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
    d=Drawing(dxfdir+'maze.svg')

    #import the maze
    matrix = json.loads( jstr )
    maze = [[Cell(x,y,matrix[x][y]) for y in range(yCells)] for x in range(xCells)]

    #what are these units?!
    transX = 5
    transY = 103 #190
    drawDXFMaze()
    d.saveas()
